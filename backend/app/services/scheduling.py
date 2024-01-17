from __future__ import annotations

import asyncio
import logging
import shutil

from beanie import PydanticObjectId

from app.config import (
    CHECK_REANA_CONNECTION_INTERVAL,
    LITTLE_NAP,
    RUN_OUTPUT_FOLDER,
    settings,
)
from app.models.experiment import Experiment
from app.models.experiment_run import ExperimentRun
from app.models.experiment_template import ExperimentTemplate
from app.routers.aiod import get_dataset_name, get_model_name
from app.schemas.experiment_run import ExperimentRunId
from app.schemas.experiment_template import ExperimentTemplateId
from app.schemas.states import RunState, TemplateState
from app.services.container_platforms.base_platform import ContainerBasePlatform
from app.services.workflow_engines.base_engine import (
    WorkflowBaseEngine,
    WorkflowConnectionExcpetion,
)


class ExperimentScheduling:
    EXPERIMENT_SCHEDULING: ExperimentScheduling | None = None

    def __init__(
        self,
        container_platform: ContainerBasePlatform,
        workflow_engine: WorkflowBaseEngine,
    ) -> None:
        self.logger = logging.getLogger("uvicorn")  # TODO should have its own logger?

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
                while not await self.workflow_engine.ping():
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
                asyncio.create_task(self.build_and_push_image(temp_id))
            await asyncio.sleep(LITTLE_NAP)

    async def execute_experiment_run(
        self, exp_run_id: PydanticObjectId
    ) -> None:  # TODO test whether it works
        async with self.experiment_semaphore:
            try:
                experiment_run = await ExperimentRun.get(exp_run_id)
                experiment = await Experiment.get(experiment_run.experiment_id)

                environment_variables = await self.general_workflow_preparation(
                    experiment_run, experiment
                )
                await self.workflow_engine.preprocess_workflow(
                    experiment_run, experiment, environment_variables
                )
                experiment_run.update_state(RunState.IN_PROGRESS)
                await experiment_run.replace()

                # TODO
                # if experiment_run is None:
                #     self.logger.info(
                #         f"ExperimentRun id={exp_run_id} has not started "
                #         + "as the corresponding docker image was not built"
                #     )
                #     return

                workflow_state = await self.workflow_engine.run_workflow(experiment_run)
                await self.workflow_engine.postprocess_workflow(experiment_run)
                await self.workflow_engine.save_metadata(experiment_run, workflow_state)

                if workflow_state.success:
                    experiment_run.update_state(RunState.FINISHED)
                    await experiment_run.replace()
                elif (
                    experiment_run.retry_count
                    < settings.MAX_EXPERIMENT_RUN_ATTEMPTS - 1
                ):
                    experiment_run.update_state(RunState.CRASHED)
                    new_exp_run = experiment_run.retry_failed_run()

                    await new_exp_run.create()
                    await experiment_run.replace()
                    await self.add_run_to_execute(new_exp_run.id)
                else:
                    experiment_run.update_state(RunState.CRASHED)
                    await experiment_run.replace()

                self.logger.info(
                    f"=== ExperimentRun id={experiment_run.id} "
                    + f"(retry_count={experiment_run.retry_count}) CONCLUDED ==="
                )
            except WorkflowConnectionExcpetion as e:
                self.logger.error(str(e))
                await self.add_run_to_execute(exp_run_id)

    async def general_workflow_preparation(
        self, experiment_run: ExperimentRun, experiment: Experiment
    ) -> dict[str, str]:
        model_names = [await get_model_name(x) for x in experiment.model_ids]
        dataset_names = [await get_dataset_name(x) for x in experiment.dataset_ids]

        environment_variables = {env.key: env.value for env in experiment.env_vars}
        environment_variables.update(
            {
                "MODEL_NAMES": ",".join(model_names),
                "DATASET_NAMES": ",".join(dataset_names),
                "METRICS": ",".join(experiment.metrics),
            }
        )

        exp_run_folder = settings.get_experiment_run_path(experiment_run.id)
        if exp_run_folder.exists():
            shutil.rmtree(exp_run_folder)
        (exp_run_folder / RUN_OUTPUT_FOLDER).mkdir(parents=True)

        return environment_variables

    async def build_and_push_image(self, template_id: PydanticObjectId) -> bool:
        async with self.image_semaphore:
            experiment_template = await ExperimentTemplate.get(template_id)

            self.logger.info(
                "=== Creation of an environment for "
                + f"ExperimentTemplate id={template_id} "
                + "INITIALIZED ==="
            )

            while True:
                experiment_template.update_state(TemplateState.IN_PROGRESS)
                await experiment_template.replace()

                image_build_state = await self.container_platform.build_image(
                    experiment_template
                )

                should_retry = (
                    experiment_template.retry_count
                    < settings.MAX_IMAGE_BUILDS_ATTEMPTS - 1
                    and image_build_state is False
                )

                if image_build_state:
                    new_state = TemplateState.FINISHED
                elif should_retry:
                    new_state = TemplateState.IN_PROGRESS
                else:
                    new_state = TemplateState.CRASHED

                experiment_template.update_state(new_state)
                experiment_template.retry_count += int(should_retry)
                await experiment_template.replace()

                if should_retry:
                    continue
                break

            self.logger.info(
                "=== Creation of an environment "
                + f"for ExperimentTemplate id={template_id} "
                + "CONCLUDED ==="
            )
            return image_build_state

    @staticmethod
    async def init(
        container_platform: ContainerBasePlatform, workflow_engine: WorkflowBaseEngine
    ) -> ExperimentScheduling:
        ExperimentScheduling.EXPERIMENT_SCHEDULING = ExperimentScheduling(
            container_platform, workflow_engine
        )
        await ExperimentScheduling.EXPERIMENT_SCHEDULING.init_image_build_queue()
        await ExperimentScheduling.EXPERIMENT_SCHEDULING.init_run_queue()

        return ExperimentScheduling.EXPERIMENT_SCHEDULING

    @staticmethod
    def get_service() -> ExperimentScheduling:
        return ExperimentScheduling.EXPERIMENT_SCHEDULING
