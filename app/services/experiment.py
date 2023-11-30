from __future__ import annotations

import asyncio
import logging

from beanie import PydanticObjectId
from docker import DockerClient

from app.config import (
    EXPERIMENT_RUN_DIR_PREFIX,
    EXPERIMENT_TEMPLATE_DIR_PREFIX,
    INTERVAL_5SEC,
    TRUE,
    settings,
)
from app.models.experiment import Experiment
from app.models.experiment_run import ExperimentRun
from app.models.experiment_template import ExperimentTemplate
from app.schemas.experiment_run import ExperimentRunId
from app.schemas.experiment_template import ExperimentTemplateId
from app.schemas.states import RunState, TemplateState
from app.services.workflow import ReanaService


class ExperimentService:
    DOCKER_SERVICE: ExperimentService | None = None

    def __init__(self) -> None:
        self.docker_client = DockerClient(base_url=settings.DOCKER_BASE_URL)
        self.logger = logging.getLogger("uvicorn")

        self.experiment_run_queue = asyncio.Queue()
        self.image_building_queue = asyncio.Queue()

        if not self.docker_registry_login():
            raise SystemExit(
                f"Unable to log in to Docker registry '{settings.DOCKER_REGISTRY_URL}'. Exiting..."
            )

        if not ReanaService.has_access():
            raise SystemExit(
                f"Unable to connect to REANA server '{settings.REANA_SERVER_URL}'. Exiting..."
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
            workflow_name = f"{EXPERIMENT_RUN_DIR_PREFIX}{str(run_id.id)}"
            try:
                ReanaService.stop_workflow(workflow_name, force_stop=True)
                ReanaService.delete_workflow(
                    workflow_name, all_runs=True, workspace=True
                )
            except Exception as e:
                self.logger.warning(
                    f"REANA Workflow of ExperimentRun id={run_id.id} "
                    + "was not successfully deleted",
                    exc_info=e,
                )

        count = self.experiment_run_queue.qsize()
        if count > 0:
            self.logger.info(
                "Workflow queue has been initialized with "
                + f"{count} workflows to execute"
            )

    async def init_image_build_queue(self) -> None:
        template_ids = (
            await ExperimentTemplate.find(
                ExperimentTemplate.approved == TRUE,
                ExperimentTemplate.state != TemplateState.FINISHED,
                ExperimentTemplate.state != TemplateState.CRASHED,
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
        return await self.experiment_run_queue.get()

    async def add_image_to_build(self, temp_id: PydanticObjectId) -> None:
        await self.image_building_queue.put(temp_id)

    async def get_image_to_build(self) -> PydanticObjectId:
        return await self.image_building_queue.get()

    async def schedule_experiment_runs(self) -> None:
        semaphore = asyncio.Semaphore(settings.MAX_PARALLEL_CONTAINERS)
        while True:
            er_id = await self.get_run_to_execute()
            asyncio.create_task(self.execute_experiment_run(er_id, semaphore))

    async def schedule_image_building(self) -> None:
        semaphore = asyncio.Semaphore(settings.MAX_PARALLEL_CONTAINERS)
        while True:
            temp_id = await self.get_image_to_build()
            asyncio.create_task(self.build_and_push_image(temp_id, semaphore))

    async def execute_experiment_run(
        self, exp_run_id: PydanticObjectId, semaphore: asyncio.Semaphore
    ) -> None:
        async with semaphore:
            experiment_run, experiment = await self.init_run(exp_run_id)

            error_msg = await ReanaService.run_workflow(experiment_run, experiment)
            await ReanaService.postprocess_workflow(experiment_run, error_msg)

            if not error_msg:
                experiment_run.update_state(RunState.FINISHED)
                await experiment_run.replace()
            elif experiment_run.retry_count < settings.MAX_EXPERIMENT_RUN_ATTEMPTS - 1:
                experiment_run.update_state(RunState.CRASHED)
                new_exp_run = experiment_run.retry_failed_run()

                await new_exp_run.create()
                await experiment_run.replace()

                await asyncio.sleep(INTERVAL_5SEC)
                await self.add_run_to_execute(new_exp_run.id)
            else:
                experiment_run.update_state(RunState.CRASHED)
                await experiment_run.replace()

            self.logger.info(
                f"=== ExperimentRun id={experiment_run.id} "
                + f"(retry_count={experiment_run.retry_count}) CONCLUDED ==="
            )

    async def init_run(
        self, exp_run_id: PydanticObjectId
    ) -> tuple[ExperimentRun, Experiment]:
        experiment_run = await ExperimentRun.get(exp_run_id)
        experiment = await Experiment.get(experiment_run.experiment_id)

        experiment_run.update_state(RunState.IN_PROGRESS)
        await experiment_run.replace()

        self.logger.info(
            f"=== ExperimentRun id={exp_run_id} "
            + f"(retry_count={experiment_run.retry_count}) "
            + f"- Experiment id={experiment.id} INITIALIZED ==="
        )
        return experiment_run, experiment

    async def build_and_push_image(
        self, template_id: PydanticObjectId, semaphore: asyncio.Semaphore
    ) -> None:
        async with semaphore:
            experiment_template = await ExperimentTemplate.get(template_id)

            image_name = f"{EXPERIMENT_TEMPLATE_DIR_PREFIX}{template_id}"
            repository_name = f"{settings.DOCKER_REGISTRY_URL}/{image_name}"
            exp_template_savepath = settings.get_experiment_template_path(
                template_id=template_id
            )

            experiment_template.update_state(TemplateState.BUILDING_IMAGE)
            await experiment_template.replace()
            self.logger.info(
                "=== Creation of an environment for "
                + f"ExperimentTemplate id={template_id} INITIALIZED ==="
            )

            try:
                self.logger.info(
                    f"\tBuilding image for ExperimentTemplate id={template_id}"
                )
                await asyncio.to_thread(
                    self.docker_client.images.build,
                    path=str(exp_template_savepath),
                    tag=f"{repository_name}",
                    pull=True,
                    rm=True,
                    nocache=False,
                )

                experiment_template.update_state(TemplateState.PUSHING_IMAGE)
                await experiment_template.replace()
                self.logger.info(
                    "\tPushing docker image to a remote repository "
                    + f"for ExperimentTemplate id={template_id}"
                )
                await asyncio.to_thread(
                    self.docker_client.images.push, repository=repository_name
                )
                self.docker_client.images.remove(repository_name)

                experiment_template.update_state(TemplateState.FINISHED)
                await experiment_template.replace()
                self.logger.info(
                    "\tDocker image has been successfully uploaded "
                    + f"for ExperimentTemplate id={template_id}"
                )
            except Exception as e:
                experiment_template.update_state(TemplateState.CRASHED)
                await experiment_template.replace()
                self.logger.error(
                    "\tThere was an error when building/pushing an image "
                    + f"for ExperimentTemplate id={template_id}",
                    exc_info=e,
                )
            self.logger.info(
                "=== Creation of an environment "
                + f"for ExperimentTemplate id={template_id} CONCLUDED ==="
            )

    @staticmethod
    async def init_docker_service() -> ExperimentService:
        ExperimentService.DOCKER_SERVICE = ExperimentService()
        await ExperimentService.DOCKER_SERVICE.init_image_build_queue()
        await ExperimentService.DOCKER_SERVICE.init_run_queue()
        return ExperimentService.DOCKER_SERVICE

    @staticmethod
    def get_docker_service() -> ExperimentService:
        return ExperimentService.DOCKER_SERVICE

    @staticmethod
    def get_image_name(experiment: Experiment) -> str:
        exp_template_id = experiment.experiment_template_id
        return f"{EXPERIMENT_TEMPLATE_DIR_PREFIX}{exp_template_id}"
