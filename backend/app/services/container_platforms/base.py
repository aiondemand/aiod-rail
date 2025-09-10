from __future__ import annotations

from abc import ABC, abstractmethod

from app.models.experiment_template import ExperimentTemplate


class ContainerPlatformBase(ABC):
    SERVICE: ContainerPlatformBase | None = None

    @abstractmethod
    async def login_to_registry(self) -> bool:
        pass

    @abstractmethod
    async def check_image(self, experiment_template: ExperimentTemplate) -> bool:
        pass

    @abstractmethod
    async def build_image(self, experiment_template: ExperimentTemplate) -> bool:
        pass

    @abstractmethod
    async def terminate(self) -> bool:
        pass

    @staticmethod
    @abstractmethod
    async def init() -> ContainerPlatformBase:
        pass

    @staticmethod
    def set_service(service: ContainerPlatformBase) -> None:
        ContainerPlatformBase.SERVICE = service

    @staticmethod
    def get_service() -> ContainerPlatformBase | None:
        return ContainerPlatformBase.SERVICE
