import asyncio
import json
import logging
import shutil
import subprocess
from pathlib import Path

from reana_client.api import client

from app.config import (
    EXPERIMENT_RUN_DIR_PREFIX,
    LOGS_FILENAME,
    METRICS_FILENAME,
    RUN_OUTPUT_FOLDER,
    RUN_TEMP_OUTPUT_FOLDER,
    settings,
)
from app.models.experiment import Experiment
from app.models.experiment_run import ExperimentRun
from app.routers.aiod import get_dataset_name, get_model_name

uvicorn_formatter = logging.getLogger("uvicorn").handlers[0].formatter
console_handler = logging.StreamHandler()
console_handler.setFormatter(uvicorn_formatter)

logger = logging.getLogger("reana")
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)


class ReanaNotConnectedException(Exception):
    pass


class ReanaService:
    @staticmethod
    def has_access() -> bool:
        for _ in range(5):
            out = client.ping(access_token=settings.REANA_ACCESS_TOKEN)
            if out["error"] is False:
                return True

        return False

    @staticmethod
    def call_reana_function(function_name, *args, **kwargs):
        if not ReanaService.has_access():
            raise ReanaNotConnectedException("Unable to connect to REANA server")
        return getattr(client, function_name)(
            *args, **kwargs, access_token=settings.REANA_ACCESS_TOKEN
        )

    @classmethod
    async def run_workflow(
        cls, experiment_run: ExperimentRun, experiment: Experiment
    ) -> str | None:
        exp_run_id = experiment_run.id

        model_names = [await get_model_name(x) for x in experiment.model_ids]
        dataset_names = [await get_dataset_name(x) for x in experiment.dataset_ids]

        environment_variables = {
            "MODEL_NAMES": ",".join(model_names),
            "DATASET_NAMES": ",".join(dataset_names),
            "METRICS": ",".join(experiment.metrics),
        }
        environment_variables.update(
            {env.key: env.value for env in experiment.env_vars}
        )

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
        workflow_name = cls.get_workflow_name(experiment_run)

        logger.info(f"\tRunning REANA workflow for ExperimentRun id={exp_run_id}")
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
                logger.error(error_log_msg)
                return error_return_msg
        except Exception as e:
            logger.error(error_log_msg, exc_info=e)
            return error_return_msg

        return None

    @classmethod
    async def postprocess_workflow(cls, experiment_run: ExperimentRun, msg_to_log: str):
        workflow_name = cls.get_workflow_name(experiment_run)
        try:
            cls.call_reana_function(
                "prune_workspace",
                workflow=workflow_name,
                include_inputs=False,
                include_outputs=False,
            )
            cls.call_reana_function(
                "mv_files",
                source=RUN_TEMP_OUTPUT_FOLDER,
                target=RUN_OUTPUT_FOLDER,
                workflow=workflow_name,
            )
            cls.save_metadata(experiment_run, msg_to_log)
        except ReanaNotConnectedException as e:
            raise e
        except Exception:
            # TODO: Handle exception properly
            pass

    @classmethod
    def save_metadata(
        cls, experiment_run: ExperimentRun, msg_to_log: str = None
    ) -> None:
        exp_output_savepath = settings.get_experiment_run_output_path(
            run_id=experiment_run.id
        )
        workflow_name = cls.get_workflow_name(experiment_run)

        logs = client.get_workflow_logs(
            workflow_name, access_token=settings.REANA_ACCESS_TOKEN
        )["logs"]

        if msg_to_log:
            logs = f"{msg_to_log}{logs}"

        exp_output_savepath.joinpath(LOGS_FILENAME).write_text(logs, encoding="utf-8")

        metrics_filepath = f"{RUN_OUTPUT_FOLDER}/{METRICS_FILENAME}"
        filenames = [
            file["name"]
            for file in client.list_files(
                workflow_name,
                file_name=metrics_filepath,
                access_token=settings.REANA_ACCESS_TOKEN,
            )
        ]
        if metrics_filepath in filenames:
            binary, _, _ = client.download_file(
                workflow_name,
                metrics_filepath,
                access_token=settings.REANA_ACCESS_TOKEN,
            )
            metrics = json.loads(binary.decode())
            with open(exp_output_savepath / METRICS_FILENAME, "w") as f:
                json.dump(metrics, f)

    @staticmethod
    def get_workflow_name(experiment_run: ExperimentRun) -> str:
        return f"{EXPERIMENT_RUN_DIR_PREFIX}{str(experiment_run.id)}"


def create_env_file(env_vars: dict[str, str], path: Path) -> None:
    lines = [f"{k}={v}" for k, v in env_vars.items()]
    path.write_text("\n".join(lines))
