from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from app.helpers import FileDetail, WorkflowState
from app.models.experiment import Experiment
from app.models.experiment_run import ExperimentRun


class WorkflowConnectionException(Exception):
    pass


class WorkflowEngineBase(ABC):
    SERVICE: WorkflowEngineBase | None = None

    @abstractmethod
    async def is_available(self) -> bool:
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
    async def stop_workflow(self, experiment_run: ExperimentRun) -> bool:
        pass

    @abstractmethod
    async def delete_workflow(self, experiment_run: ExperimentRun) -> bool:
        pass

    @abstractmethod
    async def postprocess_workflow(
        self, experiment_run: ExperimentRun, workflow_state: WorkflowState
    ) -> None:
        pass

    @abstractmethod
    async def download_file(
        self, experiment_run: ExperimentRun, filepath: str, savedir: Path
    ) -> Path | None:
        pass

    @abstractmethod
    async def list_files(self, experiment_run: ExperimentRun) -> list[FileDetail]:
        pass

    @staticmethod
    @abstractmethod
    async def init() -> WorkflowEngineBase:
        pass

    @staticmethod
    def set_service(service: WorkflowEngineBase) -> None:
        WorkflowEngineBase.SERVICE = service

    @staticmethod
    def get_service() -> WorkflowEngineBase | None:
        return WorkflowEngineBase.SERVICE
