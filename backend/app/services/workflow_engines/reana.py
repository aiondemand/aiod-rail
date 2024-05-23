from __future__ import annotations

import asyncio
import logging
import os
import re
import shutil
import subprocess
from pathlib import Path

import aiofiles as aiof
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

    async def is_available(self) -> bool:
        return self._ping()

    async def preprocess_workflow(
        self,
        experiment_run: ExperimentRun,
        experiment: Experiment,
        environment_variables: dict[str, str],
    ) -> bool:
        await self.delete_workflow(experiment)

        exp_run_folder = experiment_run.run_path
        exp_template_folder = settings.get_experiment_template_path(
            experiment.experiment_template_id
        )
        create_env_file(environment_variables, exp_run_folder / ".env")
        shutil.copy(exp_template_folder / "reana.yaml", exp_run_folder / "reana.yaml")
        shutil.copy(exp_template_folder / "script.py", exp_run_folder / "script.py")

        return True

    async def run_workflow(self, experiment_run: ExperimentRun) -> WorkflowState:
        exp_run_id = experiment_run.id
        exp_run_folder = experiment_run.run_path
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
            manually_stopped = self._is_manually_stopped(experiment_run, result.stderr)
            manually_deleted = self._is_manually_deleted(experiment_run, result.stderr)
            if manually_stopped is False and manually_deleted is False:
                self.logger.error(error_log_msg)

            return WorkflowState(
                success=False,
                error_message=error_return_msg,
                manually_stopped=manually_stopped,
                manually_deleted=manually_deleted,
            )

        return WorkflowState(success=True)

    def _is_manually_stopped(self, experiment_run: ExperimentRun, stderr: str) -> bool:
        pattern = experiment_run.workflow_name + r"\.[0-9]+ has been stopped"
        return len(re.findall(pattern, stderr)) > 0

    def _is_manually_deleted(self, experiment_run: ExperimentRun, stderr: str) -> bool:
        pattern = experiment_run.workflow_name + r".[0-9]+ has been deleted"
        return len(re.findall(pattern, stderr)) > 0

    async def stop_workflow(self, experiment_run: ExperimentRun) -> bool:
        return await self._stop_and_delete_worfklow(
            experiment_run, delete_workflow=False
        )

    async def delete_workflow(self, experiment_run: ExperimentRun) -> bool:
        return await self._stop_and_delete_worfklow(
            experiment_run, delete_workflow=True
        )

    async def _stop_and_delete_worfklow(
        self, experiment_run: ExperimentRun, delete_workflow: bool = False
    ) -> bool:
        try:
            workflow_name = experiment_run.workflow_name
            workflow_runs = await self._async_reana_call(
                "get_workflows", type="batch", workflow=workflow_name
            )
            for workflow in workflow_runs:
                if workflow["status"] == "deleted":
                    continue
                if workflow["status"] == "running":
                    await self._async_reana_call(
                        "stop_workflow", workflow=workflow_name, force_stop=True
                    )
                if delete_workflow:
                    await self._async_reana_call(
                        "delete_workflow",
                        workflow=workflow_name,
                        all_runs=True,
                        workspace=True,
                    )
        except WorkflowConnectionException as e:
            raise e
        except Exception as e:
            action = "delete" if delete_workflow else "stop"
            self.logger.error(
                f"There was error when trying to {action} a REANA workflow", exc_info=e
            )
            # TODO: Handle exception properly
            return False
        return True

    async def postprocess_workflow(
        self, experiment_run: ExperimentRun, workflow_state: WorkflowState
    ) -> None:
        workflow_name = experiment_run.workflow_name
        exp_dirpath = experiment_run.run_path
        exp_output_dirpath = experiment_run.run_output_path

        try:
            await self._async_reana_call(
                "prune_workspace",
                workflow=workflow_name,
                include_inputs=False,
                include_outputs=False,
            )
            await self._async_reana_call(
                "mv_files",
                source=RUN_TEMP_OUTPUT_FOLDER,
                target=RUN_OUTPUT_FOLDER,
                workflow=workflow_name,
            )
            # retrieve logs
            logs = (
                await self._async_reana_call(
                    "get_workflow_logs", workflow=workflow_name
                )
            )["logs"]

            if workflow_state.success is False:
                logs = f"{workflow_state.error_message}{logs}"
            exp_dirpath.joinpath(LOGS_FILENAME).write_text(logs, encoding="utf-8")
        except ReanaConnectionException as e:
            raise e
        except Exception as e:
            self.logger.error(
                "There was an error when postprocessing an experiment run", exc_info=e
            )
            return

        # save metrics.json
        metrics_filepath = f"{RUN_OUTPUT_FOLDER}/{METRICS_FILENAME}"
        await self.download_file(experiment_run, metrics_filepath, exp_output_dirpath)

    async def download_file(
        self, experiment_run: ExperimentRun, filepath: str, savedir: Path
    ) -> Path | None:
        filepath = filepath[:-1] if filepath.endswith("/") else filepath
        try:
            data, _, zipped = await self._async_reana_call(
                "download_file",
                workflow=experiment_run.workflow_name,
                file_name=filepath,
            )
        except ReanaConnectionException as e:
            raise e
        except Exception as e:
            self.logger.error(
                "There was error when trying to download a file from REANA workflow",
                exc_info=e,
            )
            return None

        savedir.mkdir(parents=True, exist_ok=True)
        filename = os.path.basename(f"{filepath}.zip" if zipped else filepath)

        async with aiof.open(savedir / filename, "wb") as f:
            await f.write(data)

        return savedir / filename

    async def list_files(self, experiment_run: ExperimentRun) -> list[FileDetail]:
        files = await self._async_reana_call(
            "list_files", workflow=experiment_run.workflow_name
        )
        return [
            FileDetail(
                filepath=file["name"],
                size=file["size"]["raw"],
                last_modified=file["last-modified"],
            )
            for file in files
        ]

    async def _async_reana_call(self, function_name, *args, **kwargs):
        return await asyncio.to_thread(self._reana_call, function_name, *args, **kwargs)

    def _ping(self) -> bool:
        for _ in range(5):
            out = client.ping(access_token=settings.REANA_ACCESS_TOKEN)
            if out["error"] is False:
                return True
        return False

    def _reana_call(self, function_name, *args, **kwargs):
        if not self._ping():
            raise ReanaConnectionException("Unable to connect to REANA server")
        return getattr(client, function_name)(
            *args, **kwargs, access_token=settings.REANA_ACCESS_TOKEN
        )

    @staticmethod
    async def init() -> ReanaService:
        service = ReanaService()

        if not await service.is_available():
            raise SystemExit(
                f"Unable to connect to REANA server '{settings.REANA_SERVER_URL}'. Exiting..."
            )
        WorkflowEngineBase.set_service(service)
        return service
