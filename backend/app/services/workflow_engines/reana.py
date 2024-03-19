from __future__ import annotations

import asyncio
import logging
import os
import shutil
import subprocess

from reana_client.api import client

from app.config import (
    LOGS_FILENAME,
    METRICS_FILENAME,
    RUN_OUTPUT_FOLDER,
    RUN_TEMP_OUTPUT_FOLDER,
    settings,
)
from app.helpers import FileDetail, WorkflowState, create_env_file
from app.models.experiment import Experiment
from app.models.experiment_run import ExperimentRun
from app.services.workflow_engines.base import (
    WorkflowConnectionException,
    WorkflowEngineBase,
)


class ReanaConnectionException(WorkflowConnectionException):
    pass


class ReanaService(WorkflowEngineBase):
    def __init__(self) -> None:
        # self.logger = setup_logging("reana")
        self.logger = logging.getLogger("uvicorn")

    async def is_connected(self) -> bool:
        return self._ping()

    async def preprocess_workflow(
        self,
        experiment_run: ExperimentRun,
        experiment: Experiment,
        environment_variables: dict[str, str],
    ) -> bool:
        try:
            # delete existing workflows tied to this experiment run if any exists
            workflow_name = experiment_run.workflow_name
            workflow_runs = await self._generic_reana_call(
                "get_workflows", type="batch", workflow=workflow_name
            )
            if len(workflow_runs) > 0:
                if workflow_runs[0]["status"] == "running":
                    await self._generic_reana_call(
                        "stop_workflow", workflow=workflow_name, force_stop=True
                    )
                await self._generic_reana_call(
                    "delete_workflow",
                    workflow=workflow_name,
                    all_runs=True,
                    workspace=True,
                )
        except WorkflowConnectionException as e:
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

        return True

    async def run_workflow(self, experiment_run: ExperimentRun) -> WorkflowState:
        exp_run_id = experiment_run.id
        exp_run_folder = settings.get_experiment_run_path(exp_run_id)
        workflow_name = experiment_run.workflow_name

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
        except Exception as e:
            self.logger.error(error_log_msg, exc_info=e)
            return WorkflowState(success=False, error_message=error_return_msg)

        if result.returncode != 0:
            self.logger.error(error_log_msg)
            return WorkflowState(success=False, error_message=error_return_msg)
        return WorkflowState(success=True)

    async def postprocess_workflow(
        self, experiment_run: ExperimentRun, workflow_state: WorkflowState
    ) -> None:
        workflow_name = experiment_run.workflow_name
        experiment_dirpath = settings.get_experiment_run_path(run_id=experiment_run.id)

        try:
            await self._generic_reana_call(
                "prune_workspace",
                workflow=workflow_name,
                include_inputs=False,
                include_outputs=False,
            )
            await self._generic_reana_call(
                "mv_files",
                source=RUN_TEMP_OUTPUT_FOLDER,
                target=RUN_OUTPUT_FOLDER,
                workflow=workflow_name,
            )
            # retrieve logs
            logs = (
                await self._generic_reana_call(
                    "get_workflow_logs", workflow=workflow_name
                )
            )["logs"]

            if workflow_state.success is False:
                logs = f"{workflow_state.error_message}{logs}"
            experiment_dirpath.joinpath(LOGS_FILENAME).write_text(
                logs, encoding="utf-8"
            )
        except ReanaConnectionException as e:
            raise e
        except Exception:
            # TODO: Handle exception properly
            pass

        # save metrics.json
        metrics_filepath = f"{RUN_OUTPUT_FOLDER}/{METRICS_FILENAME}"
        data, _ = await self.download_file(experiment_run, metrics_filepath)
        if data is not None:
            savepath_file = os.path.join(experiment_dirpath, metrics_filepath)
            os.makedirs(os.path.dirname(savepath_file), exist_ok=True)
            with open(savepath_file, "wb") as f:
                f.write(data)

    async def download_file(
        self, experiment_run: ExperimentRun, filepath: str
    ) -> tuple[bytes | None, str | None]:
        filepath = filepath[:-1] if filepath.endswith("/") else filepath
        try:
            data, _, zipped = await self._generic_reana_call(
                "download_file",
                workflow=experiment_run.workflow_name,
                file_name=filepath,
            )
        except ReanaConnectionException as e:
            raise e
        except Exception:
            return None, None

        savename = os.path.basename(f"{filepath}.zip" if zipped else filepath)
        return data, savename

    async def list_files(
        self, experiment_run: ExperimentRun, filepath: str, greater_detail: bool = False
    ) -> list[FileDetail]:
        files = await self._generic_reana_call(
            "list_files", workflow=experiment_run.workflow_name, file_name=filepath
        )
        print(files)

        pass

    async def _generic_reana_call(self, function_name, *args, **kwargs):
        return await asyncio.to_thread(
            self.__reana_call, function_name, *args, **kwargs
        )

    def _ping(self) -> bool:
        for _ in range(5):
            out = client.ping(access_token=settings.REANA_ACCESS_TOKEN)
            if out["error"] is False:
                return True
        return False

    def __reana_call(self, function_name, *args, **kwargs):
        if not self._ping():
            raise ReanaConnectionException("Unable to connect to REANA server")
        return getattr(client, function_name)(
            *args, **kwargs, access_token=settings.REANA_ACCESS_TOKEN
        )

    @staticmethod
    async def init() -> ReanaService:
        service = ReanaService()

        if not await service.is_connected():
            raise SystemExit(
                f"Unable to connect to REANA server '{settings.REANA_SERVER_URL}'. Exiting..."
            )
        WorkflowEngineBase.set_service(service)
        return service
