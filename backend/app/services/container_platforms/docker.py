from __future__ import annotations

import asyncio
import logging

from docker import DockerClient

from app.config import settings
from app.models.experiment_template import ExperimentTemplate
from app.services.container_platforms.base_platform import ContainerBasePlatform


class DockerService(ContainerBasePlatform):
    DOCKER_SERVICE: DockerService | None = None

    def __init__(self) -> None:
        self.docker_client = DockerClient(base_url=settings.DOCKER_BASE_URL)
        self.logger = logging.getLogger("uvicorn")  # TODO should have its own logger?

    async def login_to_registry(self) -> bool:
        try:
            response = self.docker_client.login(
                username=settings.DOCKER_REGISTRY_USERNAME,
                password=settings.DOCKER_REGISTRY_PASSWORD,
                registry=settings.DOCKER_REGISTRY_URL,
            )
            if response["Status"] == "Login Succeeded":
                return True
        except Exception:
            # TODO: Handle exception properly
            self.logger.exception("Error occurred while connecting to Docker registry")

        return False

    async def terminate(self) -> None:
        if self.docker_client:
            self.docker_client.close()
            self.docker_client = None

    async def build_image(self, experiment_template: ExperimentTemplate) -> bool:
        template_id = experiment_template.id
        image_name = experiment_template.get_image_name()
        exp_template_savepath = settings.get_experiment_template_path(
            template_id=template_id
        )

        try:
            self.logger.info(
                f"\tBuilding image (attempt={experiment_template.retry_count}) "
                + f"for ExperimentTemplate id={template_id}"
            )
            await asyncio.to_thread(
                self.docker_client.images.build,
                path=str(exp_template_savepath),
                tag=f"{image_name}",
                pull=True,
                rm=True,
                nocache=False,
            )

            self.logger.info(
                "\tPushing docker image to a remote repository "
                + f"for ExperimentTemplate id={template_id}"
            )
            await asyncio.to_thread(
                self.docker_client.images.push, repository=image_name
            )
            self.docker_client.images.remove(image_name)

            self.logger.info(
                "\tDocker image has been successfully uploaded "
                + f"for ExperimentTemplate id={template_id}"
            )
        except Exception as e:
            self.logger.error(
                "\tThere was an error when building/pushing an image "
                + f"for ExperimentTemplate id={template_id}",
                exc_info=e,
            )
            return False
        return True

    @staticmethod
    async def init() -> bool:
        DockerService.DOCKER_SERVICE = DockerService()

        if not await DockerService.DOCKER_SERVICE.login_to_registry():
            raise SystemExit(
                f"Unable to log in to Docker registry '{settings.DOCKER_REGISTRY_URL}'. Exiting..."
            )
        return True

    @staticmethod
    def get_service() -> DockerService:
        return DockerService.DOCKER_SERVICE
