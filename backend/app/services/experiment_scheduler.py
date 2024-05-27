from __future__ import annotations

import asyncio
import logging
import shutil

from beanie import PydanticObjectId

from app.config import CHECK_REANA_CONNECTION_INTERVAL, LITTLE_NAP, settings
from app.helpers import WorkflowState
from app.models.experiment import Experiment
from app.models.experiment_run import ExperimentRun
from app.models.experiment_template import ExperimentTemplate
from app.schemas.experiment_run import ExperimentRunId
from app.schemas.experiment_template import ExperimentTemplateId, ReservedEnvVars
from app.schemas.states import RunState, TemplateState
from app.services.aiod import get_dataset_name, get_model_name
from app.services.container_platforms.base import ContainerPlatformBase
from app.services.workflow_engines.base import (
    WorkflowConnectionException,
    WorkflowEngineBase,
)


class ExperimentScheduler:
    SERVICE: ExperimentScheduler | None = None

    def __init__(
        self,
        container_platform: ContainerPlatformBase,
        workflow_engine: WorkflowEngineBase,
    ) -> None:
        self.logger = logging.getLogger("uvicorn")

        self.container_platform = container_platform
        self.workflow_engine = workflow_engine

        self.experiment_semaphore = asyncio.Semaphore(settings.MAX_PARALLEL_CONTAINERS)
        self.image_semaphore = asyncio.Semaphore(settings.MAX_PARALLEL_IMAGE_BUILDS)

        self.experiment_run_queue = asyncio.Queue()
        self.image_building_queue = asyncio.Queue()

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

    async def add_run_to_execute(self, er_id: PydanticObjectId) -> None:
        await self.experiment_run_queue.put(er_id)

    async def get_run_to_execute(self) -> PydanticObjectId:
        while True:
            if not self.experiment_run_queue.empty():
                while not await self.workflow_engine.is_available():
                    await asyncio.sleep(CHECK_REANA_CONNECTION_INTERVAL)
                return self.experiment_run_queue.get_nowait()
            await asyncio.sleep(LITTLE_NAP)

    async def add_image_to_build(self, temp_id: PydanticObjectId) -> None:
        await self.image_building_queue.put(temp_id)

    async def get_image_to_build(self) -> PydanticObjectId:
        return await self.image_building_queue.get()

    async def schedule_experiment_runs(self) -> None:
        while True:
            if self.experiment_semaphore._value > 0:
                er_id = await self.get_run_to_execute()
                asyncio.create_task(self.execute_experiment_run(er_id))
            await asyncio.sleep(LITTLE_NAP)

    async def schedule_image_building(self) -> None:
        while True:
            if self.image_semaphore._value > 0:
                temp_id = await self.get_image_to_build()
                asyncio.create_task(self.build_experiment_environment(temp_id))
            await asyncio.sleep(LITTLE_NAP)

    async def execute_experiment_run(self, exp_run_id: PydanticObjectId) -> None:
        async with self.experiment_semaphore:
            experiment_run = await ExperimentRun.get(exp_run_id)
            experiment = await Experiment.get(experiment_run.experiment_id)
            experiment_template = await ExperimentTemplate.get(
                experiment.experiment_template_id
            )

            image_exists = await self._rebuild_image_if_necessary(
                experiment_run, experiment_template
            )
            if image_exists is False:
                return

            await experiment_run.update_state_in_db(RunState.IN_PROGRESS)
            self.logger.info(
                f"=== ExperimentRun id={experiment_run.id} "
                + f"(retry_count={experiment_run.retry_count}) "
                + f"- Experiment id={experiment.id} INITIALIZED ==="
            )
            try:
                workflow_state = await self._exec_experiment(experiment_run, experiment)
            except WorkflowConnectionException as e:
                self.logger.error(str(e))
                await self.add_run_to_execute(exp_run_id)
                return

            should_retry = (
                experiment_run.retry_count < settings.MAX_EXPERIMENT_RUN_ATTEMPTS - 1
                and workflow_state.success is False
                and workflow_state.manually_stopped is False
                and workflow_state.manually_deleted is False
            )
            if workflow_state.success:
                new_state = RunState.FINISHED
            else:
                new_state = RunState.CRASHED

            if workflow_state.manually_deleted is False:
                await experiment_run.update_state_in_db(new_state)

                if should_retry:
                    new_exp_run = experiment_run.retry_failed_run()
                    await new_exp_run.create()
                    await self.add_run_to_execute(new_exp_run.id)

            self.logger.info(
                f"=== ExperimentRun id={experiment_run.id} "
                + f"(retry_count={experiment_run.retry_count}) CONCLUDED ==="
            )

    async def _exec_experiment(
        self, experiment_run: ExperimentRun, experiment: Experiment
    ) -> WorkflowState:
        environment_variables = await self._general_workflow_preparation(
            experiment_run, experiment
        )
        await self.workflow_engine.preprocess_workflow(
            experiment_run, experiment, environment_variables
        )
        workflow_state = await self.workflow_engine.run_workflow(experiment_run)

        if workflow_state.manually_deleted is False:
            await self.workflow_engine.postprocess_workflow(
                experiment_run, workflow_state
            )
        return workflow_state

    async def _rebuild_image_if_necessary(
        self, experiment_run: ExperimentRun, experiment_template: ExperimentTemplate
    ) -> bool:
        image_exists = await self.container_platform.check_image(experiment_template)
        if image_exists:
            return True

        # image rebuilding
        await experiment_template.update_state_in_db(
            TemplateState.CREATED, retry_count=0
        )
        successful_image_rebuild = await self._build_image_multiple_attempts(
            experiment_template
        )
        if successful_image_rebuild is False:
            self.logger.error(
                f"ExperimentRun id={experiment_run.id} has not started "
                + "as the corresponding image was not successfully rebuilt"
            )
            await experiment_run.update_state_in_db(RunState.CRASHED)

        return successful_image_rebuild

    async def _general_workflow_preparation(
        self, experiment_run: ExperimentRun, experiment: Experiment
    ) -> dict[str, str]:
        model_names_env = ",".join(
            [await get_model_name(x) for x in experiment.model_ids]
        )
        dataset_names_env = ",".join(
            [await get_dataset_name(x) for x in experiment.dataset_ids]
        )
        model_ids_env = [str(id) for id in experiment.model_ids]
        dataset_ids_env = [str(id) for id in experiment.dataset_ids]
        reserved_env_values = [
            model_names_env,
            dataset_names_env,
            model_ids_env,
            dataset_ids_env,
        ]

        environment_variables = {env.key: env.value for env in experiment.env_vars}
        reserved_vars = {
            name.value: val
            for name, val in zip(list(ReservedEnvVars), reserved_env_values)
        }
        environment_variables.update(reserved_vars)

        exp_run_folder = experiment_run.run_path
        if exp_run_folder.exists():
            shutil.rmtree(exp_run_folder)
        exp_run_folder.mkdir(parents=True)

        return environment_variables

    async def build_experiment_environment(self, template_id: PydanticObjectId) -> bool:
        async with self.image_semaphore:
            experiment_template = await ExperimentTemplate.get(template_id)

            self.logger.info(
                "=== Creation of an environment for "
                + f"ExperimentTemplate id={template_id} "
                + "INITIALIZED ==="
            )
            image_build_state = await self._build_image_multiple_attempts(
                experiment_template
            )
            self.logger.info(
                "=== Creation of an environment "
                + f"for ExperimentTemplate id={template_id} "
                + "CONCLUDED ==="
            )
            return image_build_state

    async def _build_image_multiple_attempts(
        self, experiment_template: ExperimentTemplate
    ) -> bool:
        while True:
            await experiment_template.update_state_in_db(TemplateState.IN_PROGRESS)

            image_build_state = await self.container_platform.build_image(
                experiment_template
            )
            should_retry = (
                experiment_template.retry_count < settings.MAX_IMAGE_BUILDS_ATTEMPTS - 1
                and image_build_state is False
            )

            if image_build_state:
                new_state = TemplateState.FINISHED
            elif should_retry:
                new_state = TemplateState.IN_PROGRESS
            else:
                new_state = TemplateState.CRASHED

            await experiment_template.update_state_in_db(
                new_state,
                retry_count=experiment_template.retry_count + int(should_retry),
            )
            if should_retry:
                continue
            return image_build_state

    @staticmethod
    async def init(
        container_platform: ContainerPlatformBase, workflow_engine: WorkflowEngineBase
    ) -> ExperimentScheduler:
        ExperimentScheduler.SERVICE = ExperimentScheduler(
            container_platform, workflow_engine
        )
        await ExperimentScheduler.SERVICE.init_image_build_queue()
        await ExperimentScheduler.SERVICE.init_run_queue()

        return ExperimentScheduler.SERVICE

    @staticmethod
    def get_service() -> ExperimentScheduler:
        return ExperimentScheduler.SERVICE
