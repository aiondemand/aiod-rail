from __future__ import annotations

import asyncio
import json
import logging
import shutil
import subprocess

from beanie import PydanticObjectId
from docker import DockerClient
from reana_client.api import client as reana

from app.config import (
    EXPERIMENT_RUN_DIR_PREFIX,
    EXPERIMENT_TEMPLATE_DIR_PREFIX,
    INTERVAL_5SEC,
    LOGS_FILENAME,
    METRICS_FILENAME,
    RUN_OUTPUT_FOLDER,
    RUN_TEMP_OUTPUT_FOLDER,
    settings,
)
from app.models.experiment import Experiment
from app.models.experiment_run import ExperimentRun
from app.models.experiment_template import ExperimentTemplate
from app.routers.aiod import get_dataset_name, get_model_name
from app.schemas.experiment_run import ExperimentRunId
from app.schemas.experiment_template import ExperimentTemplateId
from app.schemas.states import RunState, TemplateState

REANA_TOKEN_KW = {"access_token": settings.REANA_ACCESS_TOKEN}


class ExperimentService:
    DOCKER_SERVICE: ExperimentService | None = None

    def __init__(self) -> None:
        self.docker_client = DockerClient(base_url=settings.DOCKER_BASE_URL)
        self.logger = logging.getLogger("uvicorn")

        self.experiment_run_queue = asyncio.Queue()
        self.image_building_queue = asyncio.Queue()

        docker_login_success = False
        try:
            response = self.docker_client.login(
                username=settings.DOCKER_REGISTRY_USERNAME,
                password=settings.DOCKER_REGISTRY_PASSWORD,
            )
            if response["Status"] == "Login Succeeded":
                docker_login_success = True
        except Exception:
            # TODO: Handle exception properly
            pass

        if not docker_login_success:
            self.logger.error(
                f"Unable to log in to Docker registry '{settings.DOCKER_REGISTRY_URL}'. Exiting..."
            )
            exit(1)

        for _ in range(5):
            out = reana.ping(**REANA_TOKEN_KW)
            if out["error"] is False:
                break
        else:
            self.logger.error(
                f"Unable to connect to REANA server '{settings.REANA_SERVER_URL}'. Exiting..."
            )
            exit(1)

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
                reana.stop_workflow(workflow_name, force_stop=True, **REANA_TOKEN_KW)
                reana.delete_workflow(
                    workflow_name, all_runs=True, workspace=True, **REANA_TOKEN_KW
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
        run_ids = (
            await ExperimentTemplate.find(
                ExperimentTemplate.state != TemplateState.FINISHED,
                ExperimentTemplate.state != TemplateState.CRASHED,
            )
            .sort(+ExperimentTemplate.updated_at)
            .project(ExperimentTemplateId)
            .to_list()
        )
        for run_id in run_ids:
            await self.add_image_to_build(run_id.id)

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

            error_msg = await self.run_workflow(experiment_run, experiment)
            await self.postprocess_workflow(experiment_run, error_msg)

    async def init_run(
        self, exp_run_id: PydanticObjectId
    ) -> tuple[ExperimentRun, Experiment]:
        experiment_run = await ExperimentRun.get(exp_run_id)
        experiment = await Experiment.get(experiment_run.experiment_id)

        experiment_run.update_state(RunState.IN_PROGRESS)
        await experiment_run.replace()

        self.logger.info(
            f"=== ExperimentRun id={exp_run_id} "
            + f"(run_number={experiment_run.run_number}) "
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

    async def run_workflow(
        self, experiment_run: ExperimentRun, experiment: Experiment
    ) -> str:
        exp_run_id = experiment_run.id

        model_names = [await get_model_name(x) for x in experiment.model_ids]
        dataset_names = [await get_dataset_name(x) for x in experiment.dataset_ids]

        environment_variables = {
            "MODEL_NAMES": ",".join(model_names),
            "DATASET_NAMES": ",".join(dataset_names),
            "METRICS": ",".join(experiment.metrics),
        }
        environment_variables.update(experiment.env_vars)

        exp_run_folder = settings.get_experiment_run_path(exp_run_id)
        exp_template_folder = settings.get_experiment_template_path(
            experiment.experiment_template_id
        )
        if exp_run_folder.exists():
            shutil.rmtree(exp_run_folder)
        (exp_run_folder / RUN_OUTPUT_FOLDER).mkdir(parents=True)

        create_env_file(environment_variables, exp_run_folder / ".env")
        shutil.copy(exp_template_folder / "reana.yaml", exp_run_folder / "reana.yaml")
        shutil.copy(exp_template_folder / "script.py", exp_run_folder / "script.py")
        workflow_name = ExperimentService.get_workflow_name(experiment_run)

        self.logger.info(f"\tRunning REANA workflow for ExperimentRun id={exp_run_id}")
        error_log_msg = (
            "\tThere was an error when running REANA workflow "
            + f"for ExperimentRun id={exp_run_id}"
        )
        error_return_msg = "Error encountered when running a REANA workflow.\n\n"

        try:
            reana_command = f"reana-client run -w {workflow_name} --follow"
            result = await asyncio.to_thread(
                subprocess.run,
                f"cd {exp_run_folder}; {reana_command}",
                capture_output=True,
                shell=True,
                text=True,
            )
            if result.returncode != 0:
                self.logger.error(error_log_msg)
                return error_return_msg
        except Exception as e:
            self.logger.error(error_log_msg, exc_info=e)
            return error_return_msg

        return ""

    async def postprocess_workflow(
        self, experiment_run: ExperimentRun, error_msg: str
    ) -> None:
        workflow_name = ExperimentService.get_workflow_name(experiment_run)
        reana.prune_workspace(
            workflow_name, include_inputs=False, include_outputs=False, **REANA_TOKEN_KW
        )
        try:
            reana.mv_files(
                RUN_TEMP_OUTPUT_FOLDER,
                RUN_OUTPUT_FOLDER,
                workflow_name,
                **REANA_TOKEN_KW,
            )
        except Exception:
            # TODO: Handle exception properly
            pass

        self.save_metadata(experiment_run, error_msg)

        if len(error_msg) == 0:
            experiment_run.update_state(RunState.FINISHED)
            await experiment_run.replace()
        elif experiment_run.run_number < settings.MAX_EXPERIMENT_RUN_ATTEMPTS - 1:
            experiment_run.update_state(RunState.CRASHED)
            new_exp_run = experiment_run.create_following_run()

            await new_exp_run.create()
            await experiment_run.replace()

            await asyncio.sleep(INTERVAL_5SEC)
            await self.add_run_to_execute(new_exp_run.id)
        else:
            experiment_run.update_state(RunState.CRASHED)
            await experiment_run.replace()

        self.logger.info(
            f"=== ExperimentRun id={experiment_run.id} "
            + f"(run_number={experiment_run.run_number}) CONCLUDED ==="
        )

    @staticmethod
    def save_metadata(experiment_run: ExperimentRun, error_msg: str = "") -> None:
        exp_output_savepath = settings.get_experiment_run_output_path(
            run_id=experiment_run.id
        )
        workflow_name = ExperimentService.get_workflow_name(experiment_run)

        logs = reana.get_workflow_logs(workflow_name, **REANA_TOKEN_KW)["logs"]
        if len(error_msg) > 0:
            logs = f"{error_msg}{logs}"
        log_filepath = exp_output_savepath / LOGS_FILENAME
        with open(log_filepath, "w", encoding="utf-8") as f:
            f.write(logs)

        metrics_filepath = f"{RUN_OUTPUT_FOLDER}/{METRICS_FILENAME}"
        filenames = [
            file["name"]
            for file in reana.list_files(
                workflow_name, file_name=metrics_filepath, **REANA_TOKEN_KW
            )
        ]
        if metrics_filepath in filenames:
            binary, _, _ = reana.download_file(
                workflow_name, metrics_filepath, **REANA_TOKEN_KW
            )
            metrics = json.loads(binary.decode())
            with open(exp_output_savepath / METRICS_FILENAME, "w") as f:
                json.dump(metrics, f)

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
    def get_workflow_name(experiment_run: ExperimentRun) -> str:
        return f"{EXPERIMENT_RUN_DIR_PREFIX}{str(experiment_run.id)}"

    @staticmethod
    def get_image_name(experiment: Experiment) -> str:
        exp_template_id = experiment.experiment_template_id
        return f"{EXPERIMENT_TEMPLATE_DIR_PREFIX}{exp_template_id}"


def create_env_file(env_vars, path) -> None:
    lines = []
    for k, v in env_vars.items():
        lines.append(f"{k}={v}\n")

    with open(path, "w") as f:
        f.writelines(lines)
