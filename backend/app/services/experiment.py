from __future__ import annotations

import asyncio
import logging

from beanie import PydanticObjectId
from docker import DockerClient
from docker.errors import APIError

from app.config import INTERVAL_1MIN, INTERVAL_5SEC, settings
from app.models.experiment import Experiment
from app.models.experiment_run import ExperimentRun
from app.models.experiment_template import ExperimentTemplate
from app.schemas.experiment_run import ExperimentRunId
from app.schemas.experiment_template import ExperimentTemplateId
from app.schemas.states import RunState, TemplateState
from app.services.workflow import ReanaNotConnectedException, ReanaService


class ExperimentService:
    DOCKER_SERVICE: ExperimentService | None = None

    def __init__(self) -> None:
        self.docker_client = DockerClient(base_url=settings.DOCKER_BASE_URL)
        self.logger = logging.getLogger("uvicorn")

        self.experiment_semaphore = asyncio.Semaphore(settings.MAX_PARALLEL_CONTAINERS)
        self.image_semaphore = asyncio.Semaphore(settings.MAX_PARALLEL_IMAGE_BUILDS)

        self.experiment_run_queue = asyncio.Queue()
        self.image_building_queue = asyncio.Queue()

        if not self.docker_registry_login():
            raise SystemExit(
                f"Unable to log in to Docker registry '{settings.DOCKER_REGISTRY_URL}'. Exiting..."
            )

    def docker_registry_login(self) -> bool:
        try:
            response = self.docker_client.login(
                username=settings.DOCKER_REGISTRY_USERNAME,
                password=settings.DOCKER_REGISTRY_PASSWORD,
                registry=settings.DOCKER_REGISTRY_URL,
            )
            if response["Status"] == "Login Succeeded":
                return True
        except Exception:
            # TODO: Handle exception properly
            self.logger.exception("Error occurred while connecting to Docker registry")

        return False

    async def init_run_queue(self) -> None:
        run_ids = (
            await ExperimentRun.find(
                ExperimentRun.state != RunState.FINISHED,
                ExperimentRun.state != RunState.CRASHED,
            )
            .sort(+ExperimentRun.updated_at)
            .project(ExperimentRunId)
            .to_list()
        )
        for run_id in run_ids:
            await self.add_run_to_execute(run_id.id)

        count = self.experiment_run_queue.qsize()
        if count > 0:
            self.logger.info(
                "Workflow queue has been initialized with "
                + f"{count} workflows to execute"
            )

    async def init_image_build_queue(self) -> None:
        template_ids = (
            await ExperimentTemplate.find(
                ExperimentTemplate.approved == True,  # noqa: E712
                ExperimentTemplate.state != TemplateState.FINISHED,
                ExperimentTemplate.state != TemplateState.CRASHED,
                ExperimentTemplate.retry_count < settings.MAX_IMAGE_BUILDS_ATTEMPTS,
            )
            .sort(+ExperimentTemplate.updated_at)
            .project(ExperimentTemplateId)
            .to_list()
        )
        for template_id in template_ids:
            await self.add_image_to_build(template_id.id)

        count = self.image_building_queue.qsize()
        if count > 0:
            self.logger.info(
                "Docker image queue has been initialized with "
                + f"{count} images to build and push"
            )

    def close_docker_connection(self) -> None:
        if self.docker_client:
            self.docker_client.close()

    # TODO
    def download_files(self) -> None:
        pass

    # TODO
    def list_files(self) -> None:
        pass

    async def add_run_to_execute(self, er_id: PydanticObjectId) -> None:
        await self.experiment_run_queue.put(er_id)

    async def get_run_to_execute(self) -> PydanticObjectId:
        while True:
            if not self.experiment_run_queue.empty():
                # check whether REANA is accessible
                while not ReanaService.has_access():
                    await asyncio.sleep(INTERVAL_1MIN)
                return self.experiment_run_queue.get_nowait()
            await asyncio.sleep(INTERVAL_5SEC)

    async def add_image_to_build(self, temp_id: PydanticObjectId) -> None:
        await self.image_building_queue.put(temp_id)

    async def get_image_to_build(self) -> PydanticObjectId:
        return await self.image_building_queue.get()

    async def schedule_experiment_runs(self) -> None:
        while True:
            if self.experiment_semaphore._value > 0:
                er_id = await self.get_run_to_execute()
                asyncio.create_task(self.execute_experiment_run(er_id))
            await asyncio.sleep(INTERVAL_5SEC)

    async def schedule_image_building(self) -> None:
        while True:
            if self.image_semaphore._value > 0:
                temp_id = await self.get_image_to_build()
                asyncio.create_task(self.build_and_push_image(temp_id))
            await asyncio.sleep(INTERVAL_5SEC)

    async def execute_experiment_run(self, exp_run_id: PydanticObjectId) -> None:
        async with self.experiment_semaphore:
            try:
                experiment_run, experiment = await self.init_run(exp_run_id)
                if experiment_run is None:
                    return

                # run the experiment by executing REANA workflow
                error_msg = await ReanaService.run_workflow(experiment_run, experiment)
                # process the workflow output
                await ReanaService.postprocess_workflow(experiment_run, error_msg)

                if not error_msg:
                    # everything went smoothly
                    experiment_run.update_state(RunState.FINISHED)
                    await experiment_run.replace()
                elif (
                    experiment_run.retry_count
                    < settings.MAX_EXPERIMENT_RUN_ATTEMPTS - 1
                ):
                    # if an error occured retry for X amount of times
                    # we use a new experiment run object for retries
                    experiment_run.update_state(RunState.CRASHED)
                    new_exp_run = experiment_run.retry_failed_run()

                    await new_exp_run.create()
                    await experiment_run.replace()
                    await self.add_run_to_execute(new_exp_run.id)
                else:
                    # if an error occured and we have spent all the retries
                    # we dont bother with retrying the experiment again
                    experiment_run.update_state(RunState.CRASHED)
                    await experiment_run.replace()

                self.logger.info(
                    f"=== ExperimentRun id={experiment_run.id} "
                    + f"(retry_count={experiment_run.retry_count}) CONCLUDED ==="
                )
            except ReanaNotConnectedException as e:
                # during the execution of the experiment we lost the connection
                # to the REANA server
                # to delete potentially existing workflow of the current
                # experiment run, we will use the same experiment run object
                self.logger.error(str(e))
                await self.add_run_to_execute(exp_run_id)

    async def init_run(
        self, exp_run_id: PydanticObjectId
    ) -> tuple[ExperimentRun, Experiment]:
        experiment_run = await ExperimentRun.get(exp_run_id)
        experiment = await Experiment.get(experiment_run.experiment_id)

        workflow_name = ReanaService.get_workflow_name(experiment_run)

        try:
            workflow_runs = ReanaService.call_reana_function(
                "get_workflows", type="batch", workflow=workflow_name
            )
            if len(workflow_runs) > 0:
                if workflow_runs[0]["status"] == "running":
                    ReanaService.call_reana_function(
                        "stop_workflow", workflow=workflow_name, force_stop=True
                    )
                ReanaService.call_reana_function(
                    "delete_workflow",
                    workflow=workflow_name,
                    all_runs=True,
                    workspace=True,
                )
        except ReanaNotConnectedException as e:
            raise e
        except Exception as e:
            self.logger.warning(
                f"REANA Workflow of ExperimentRun id={experiment_run.id} "
                + "was not successfully deleted",
                exc_info=e,
            )

        # check whether docker image exists, and if not, rebuild it again
        experiment_template = await ExperimentTemplate.get(
            experiment.experiment_template_id
        )
        image_name = experiment_template.get_image_name()
        try:
            self.docker_client.images.get_registry_data(image_name)
        except APIError:
            self.logger.warning(
                "Docker image for ExperimentTemplate "
                + f"id={experiment_template.id} was not found. "
                + "Rebuilding the image..."
            )
            experiment_template.retry_count = 0
            experiment_template.state = TemplateState.CREATED
            await experiment_template.replace()

            successful_image_build = await self.build_and_push_image(
                experiment_template.id
            )
            if not successful_image_build:
                # since we were not able to rebuild an image, we conclude this
                # experiment run -> we dont even attempt to retry it
                experiment_run.update_state(RunState.CRASHED)
                await experiment_run.replace()
                return None, None

        experiment_run.update_state(RunState.IN_PROGRESS)
        await experiment_run.replace()

        self.logger.info(
            f"=== ExperimentRun id={exp_run_id} "
            + f"(retry_count={experiment_run.retry_count}) "
            + f"- Experiment id={experiment.id} INITIALIZED ==="
        )
        return experiment_run, experiment

    async def build_and_push_image(self, template_id: PydanticObjectId) -> bool:
        async with self.image_semaphore:
            experiment_template = await ExperimentTemplate.get(template_id)

            successful_image_build = True
            image_name = experiment_template.get_image_name()
            exp_template_savepath = settings.get_experiment_template_path(
                template_id=template_id
            )
            self.logger.info(
                "=== Creation of an environment for "
                + f"ExperimentTemplate id={template_id} "
                + "INITIALIZED ==="
            )

            while True:
                experiment_template.update_state(TemplateState.IN_PROGRESS)
                await experiment_template.replace()

                try:
                    self.logger.info(
                        f"\tBuilding image (attempt={experiment_template.retry_count}) "
                        + f"for ExperimentTemplate id={template_id}"
                    )
                    await asyncio.to_thread(
                        self.docker_client.images.build,
                        path=str(exp_template_savepath),
                        tag=f"{image_name}",
                        pull=True,
                        rm=True,
                        nocache=False,
                    )

                    self.logger.info(
                        "\tPushing docker image to a remote repository "
                        + f"for ExperimentTemplate id={template_id}"
                    )
                    await asyncio.to_thread(
                        self.docker_client.images.push, repository=image_name
                    )
                    self.docker_client.images.remove(image_name)

                    experiment_template.update_state(TemplateState.FINISHED)
                    await experiment_template.replace()
                    self.logger.info(
                        "\tDocker image has been successfully uploaded "
                        + f"for ExperimentTemplate id={template_id}"
                    )
                except Exception as e:
                    self.logger.error(
                        "\tThere was an error when building/pushing an image "
                        + f"for ExperimentTemplate id={template_id}",
                        exc_info=e,
                    )
                    if (
                        experiment_template.retry_count
                        < settings.MAX_IMAGE_BUILDS_ATTEMPTS - 1
                    ):
                        experiment_template.retry_count += 1
                        await experiment_template.replace()
                        continue

                    successful_image_build = False
                    experiment_template.update_state(TemplateState.CRASHED)
                    await experiment_template.replace()

                self.logger.info(
                    "=== Creation of an environment "
                    + f"for ExperimentTemplate id={template_id} "
                    + "CONCLUDED ==="
                )
                return successful_image_build

    @staticmethod
    async def init_docker_service() -> ExperimentService:
        ExperimentService.DOCKER_SERVICE = ExperimentService()
        await ExperimentService.DOCKER_SERVICE.init_image_build_queue()
        await ExperimentService.DOCKER_SERVICE.init_run_queue()
        return ExperimentService.DOCKER_SERVICE

    @staticmethod
    def get_docker_service() -> ExperimentService:
        return ExperimentService.DOCKER_SERVICE
