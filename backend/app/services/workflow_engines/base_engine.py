from __future__ import annotations

from abc import ABC, abstractmethod, abstractstaticmethod

from app.helpers import WorkflowState
from app.models.experiment import Experiment
from app.models.experiment_run import ExperimentRun


class WorkflowConnectionExcpetion(Exception):
    pass


class WorkflowBaseEngine(ABC):
    @abstractmethod
    async def ping(self) -> bool:
        pass

    @abstractmethod
    async def preprocess_workflow(
        self,
        experiment_run: ExperimentRun,
        experiment: Experiment,
        environment_variables: dict[str, str],
    ) -> bool:
        pass

    @abstractmethod
    async def run_workflow(self, experiment_run: ExperimentRun) -> WorkflowState:
        pass

    @abstractmethod
    async def postprocess_workflow(self, experiment_run: ExperimentRun) -> bool:
        pass

    @abstractmethod
    async def download_files(
        self, experiment_run: ExperimentRun, filepath: str, is_directory: bool = False
    ) -> bool:
        pass

    @abstractmethod
    async def save_metadata(
        self, experiment_run: ExperimentRun, workflow_state: WorkflowState
    ) -> bool:
        pass

    @abstractstaticmethod
    def get_workflow_name(experiment_run: ExperimentRun) -> str:
        pass

    @abstractstaticmethod
    async def init() -> WorkflowBaseEngine:
        pass

    @abstractstaticmethod
    def get_service() -> WorkflowBaseEngine:
        pass
