from __future__ import annotations

from abc import ABC, abstractmethod, abstractstaticmethod

from app.models.experiment_template import ExperimentTemplate


class ContainerBasePlatform(ABC):
    SERVICE: ContainerBasePlatform | None = None

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

    @abstractstaticmethod
    async def init() -> ContainerBasePlatform:
        pass

    @staticmethod
    def set_service(service: ContainerBasePlatform) -> None:
        ContainerBasePlatform.SERVICE = service

    @staticmethod
    def get_service() -> ContainerBasePlatform:
        return ContainerBasePlatform.SERVICE
