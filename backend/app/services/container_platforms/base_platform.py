from __future__ import annotations

from abc import ABC, abstractmethod, abstractstaticmethod

from app.models.experiment_template import ExperimentTemplate


class ContainerBasePlatform(ABC):
    @abstractmethod
    async def login_to_registry(self) -> bool:
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

    @abstractstaticmethod
    def get_service() -> ContainerBasePlatform:
        pass
