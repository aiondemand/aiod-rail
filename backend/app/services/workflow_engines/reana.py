from __future__ import annotations

import asyncio
import json
import logging
import shutil
import subprocess

from reana_client.api import client

from app.config import (
    EXPERIMENT_RUN_DIR_PREFIX,
    LOGS_FILENAME,
    METRICS_FILENAME,
    RUN_OUTPUT_FOLDER,
    RUN_TEMP_OUTPUT_FOLDER,
    settings,
)
from app.helpers import WorkflowState, create_env_file
from app.models.experiment import Experiment
from app.models.experiment_run import ExperimentRun
from app.services.workflow_engines.base_engine import (
    WorkflowBaseEngine,
    WorkflowConnectionExcpetion,
)


class ReanaConnectionException(WorkflowConnectionExcpetion):
    pass


class ReanaService(WorkflowBaseEngine):
    REANA_SERVICE: ReanaService | None = None

    def __init__(self) -> None:
        self.logger = logging.getLogger("uvicorn")  # TODO should have its own logger?

    async def ping(self) -> bool:
        for _ in range(5):
            out = client.ping(access_token=settings.REANA_ACCESS_TOKEN)
            if out["error"] is False:
                return True

        return False

    async def preprocess_workflow(
        self,
        experiment_run: ExperimentRun,
        experiment: Experiment,
        environment_variables: dict[str, str],
    ) -> bool:
        workflow_name = self.get_workflow_name(experiment_run)

        # delete existing workflows tied to this experiment run if any exists
        try:
            workflow_runs = await self._call_reana_function(
                "get_workflows", type="batch", workflow=workflow_name
            )
            if len(workflow_runs) > 0:
                if workflow_runs[0]["status"] == "running":
                    await self._call_reana_function(
                        "stop_workflow", workflow=workflow_name, force_stop=True
                    )
                await self._call_reana_function(
                    "delete_workflow",
                    workflow=workflow_name,
                    all_runs=True,
                    workspace=True,
                )
        except WorkflowConnectionExcpetion as e:
            raise e
        except Exception as e:
            self.logger.warning(
                f"REANA Workflow of ExperimentRun id={experiment_run.id} "
                + "was not successfully deleted",
                exc_info=e,
            )

        exp_run_folder = settings.get_experiment_run_path(experiment_run.id)
        exp_template_folder = settings.get_experiment_template_path(
            experiment.experiment_template_id
        )

        create_env_file(environment_variables, exp_run_folder / ".env")
        shutil.copy(exp_template_folder / "reana.yaml", exp_run_folder / "reana.yaml")
        shutil.copy(exp_template_folder / "script.py", exp_run_folder / "script.py")

        # TODO this needs to be covered later on

        # # check whether docker image exists, and if not, rebuild it again
        # experiment_template = await ExperimentTemplate.get(
        #     experiment.experiment_template_id
        # )
        # image_name = experiment_template.get_image_name()
        # try:
        #     self.docker_client.images.get_registry_data(image_name)
        # except APIError:
        #     self.logger.warning(
        #         "Docker image for ExperimentTemplate "
        #         + f"id={experiment_template.id} was not found. "
        #         + "Rebuilding the image..."
        #     )
        #     experiment_template.retry_count = 0
        #     experiment_template.state = TemplateState.CREATED
        #     await experiment_template.replace()

        #     # TODO this implementation is flawed as if our application crashes
        #     # while the image is being built in this stage, we end up with 1 unfinished
        #     # experiment template image building and 1 experiment run,
        #     # hence once we start up the application again, both processes will
        #     # run in parallel and effectively we will build the same image twice
        #     # in the same time, which is not ideal...
        #     successful_image_build = await self.build_and_push_image(
        #         experiment_template.id
        #     )
        #     if not successful_image_build:
        #         # since we were not able to rebuild an image, we conclude this
        #         # experiment run -> we dont even attempt to retry it
        #         experiment_run.update_state(RunState.CRASHED)
        #         await experiment_run.replace()
        #         return None, None

        self.logger.info(
            f"=== ExperimentRun id={experiment_run.id} "
            + f"(retry_count={experiment_run.retry_count}) "
            + f"- Experiment id={experiment.id} INITIALIZED ==="
        )
        return True

    async def run_workflow(self, experiment_run: ExperimentRun) -> WorkflowState:
        exp_run_id = experiment_run.id
        exp_run_folder = settings.get_experiment_run_path(exp_run_id)
        workflow_name = self.get_workflow_name(experiment_run)

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
                return WorkflowState(success=False, error_message=error_return_msg)
        except Exception as e:
            self.logger.error(error_log_msg, exc_info=e)
            return WorkflowState(success=False, error_message=error_return_msg)
        return WorkflowState(success=True)

    async def postprocess_workflow(self, experiment_run: ExperimentRun) -> bool:
        workflow_name = self.get_workflow_name(experiment_run)
        try:
            await self._call_reana_function(
                "prune_workspace",
                workflow=workflow_name,
                include_inputs=False,
                include_outputs=False,
            )
            await self._call_reana_function(
                "mv_files",
                source=RUN_TEMP_OUTPUT_FOLDER,
                target=RUN_OUTPUT_FOLDER,
                workflow=workflow_name,
            )
        except ReanaConnectionException as e:
            raise e
        except Exception:
            # TODO: Handle exception properly
            pass

    # TODO later
    async def download_files(
        self, experiment_run: ExperimentRun, filepath: str, is_directory: bool = False
    ) -> bool:
        # workflow_name = self.get_workflow_name(experiment_run)
        try:
            pass
        except ReanaConnectionException as e:
            raise e
        except Exception:
            # TODO: Handle exception properly
            pass
        return True

    async def save_metadata(
        self, experiment_run: ExperimentRun, workflow_state: WorkflowState
    ) -> bool:
        workflow_name = self.get_workflow_name(experiment_run)
        exp_output_savepath = settings.get_experiment_run_output_path(
            run_id=experiment_run.id
        )

        # retrieve logs
        try:
            logs = (
                await self._call_reana_function(
                    "get_workflow_logs", workflow=workflow_name
                )
            )["logs"]

            if workflow_state.success is False:
                logs = f"{workflow_state.error_message}{logs}"
            exp_output_savepath.joinpath(LOGS_FILENAME).write_text(
                logs, encoding="utf-8"
            )
        except ReanaConnectionException as e:
            raise e
        except Exception:
            # TODO: Handle exception properly
            pass

        # save metrics.json
        try:
            metrics_filepath = f"{RUN_OUTPUT_FOLDER}/{METRICS_FILENAME}"
            matched_files = await self._call_reana_function(
                "list_files", workflow=workflow_name, file_name=metrics_filepath
            )
            if len(matched_files) > 0 and matched_files[0]["name"] == metrics_filepath:
                binary, _, _ = await self._call_reana_function(
                    "download_file", workflow=workflow_name, file_name=metrics_filepath
                )
                metrics = json.loads(binary.decode())
                with open(exp_output_savepath / METRICS_FILENAME, "w") as f:
                    json.dump(metrics, f)

        except ReanaConnectionException as e:
            raise e
        except Exception:
            # TODO: Handle exception properly
            pass

        return True

    async def _call_reana_function(self, function_name, *args, **kwargs):
        if not await self.ping():
            raise ReanaConnectionException("Unable to connect to REANA server")
        return getattr(client, function_name)(
            *args, **kwargs, access_token=settings.REANA_ACCESS_TOKEN
        )

    @staticmethod
    def get_workflow_name(experiment_run: ExperimentRun) -> str:
        return f"{EXPERIMENT_RUN_DIR_PREFIX}{str(experiment_run.id)}"

    @staticmethod
    async def init() -> ReanaService:
        ReanaService.REANA_SERVICE = ReanaService()

        if not await ReanaService.REANA_SERVICE.ping():
            raise SystemExit(
                f"Unable to log in to Docker registry '{settings.DOCKER_REGISTRY_URL}'. Exiting..."
            )
        return ReanaService.REANA_SERVICE

    @staticmethod
    def get_service() -> ReanaService:
        return ReanaService.REANA_SERVICE
