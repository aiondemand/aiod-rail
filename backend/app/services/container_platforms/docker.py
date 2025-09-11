from __future__ import annotations

import asyncio
import logging

from docker import DockerClient
from docker.errors import APIError

from app.config import settings
from app.models.experiment_template import ExperimentTemplate
from app.services.container_platforms.base import ContainerPlatformBase


class DockerService(ContainerPlatformBase):
    def __init__(self) -> None:
        self.docker_client = DockerClient(base_url=settings.DOCKER_BASE_URL)
        # self.logger = setup_logging("docker")
        self.logger = logging.getLogger("uvicorn")

    async def login_to_registry(self) -> bool:
        try:
            response = await asyncio.to_thread(
                self.docker_client.login,
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

    async def terminate(self) -> bool:
        if self.docker_client:
            self.docker_client.close()
            self.docker_client = None

        return True

    async def check_image(self, experiment_template: ExperimentTemplate) -> bool:
        try:
            await asyncio.to_thread(
                self.docker_client.images.get_registry_data,
                experiment_template.image_name,
            )
        except APIError:
            self.logger.warning(
                "Docker image for ExperimentTemplate "
                + f"id={experiment_template.id} was not found. "
                + "Rebuilding the image..."
            )
            return False
        return True

    async def build_image(self, experiment_template: ExperimentTemplate) -> bool:
        template_id = experiment_template.id
        image_name = experiment_template.image_name
        template_path = experiment_template.experiment_template_path

        self.logger.info(
            f"\tBuilding image (attempt={experiment_template.retry_count}) "
            + f"for ExperimentTemplate id={template_id}"
        )

        try:
            await asyncio.to_thread(
                self.docker_client.images.build,
                path=str(template_path),
                tag=f"{image_name}",
                pull=True,
                rm=True,
                nocache=False,
            )
            self.logger.info(
                "\tPushing docker image to a remote repository "
                + f"for ExperimentTemplate id={template_id}"
            )
            # TODO perhaps we need to remove the already existing image first

            await asyncio.to_thread(self.docker_client.images.push, repository=image_name)
            await asyncio.to_thread(self.docker_client.images.remove, image=image_name)
        except Exception as e:
            self.logger.error(
                "\tThere was an error when building/pushing an image "
                + f"for ExperimentTemplate id={template_id}",
                exc_info=e,
            )
            return False

        self.logger.info(
            "\tDocker image has been successfully uploaded "
            + f"for ExperimentTemplate id={template_id}"
        )
        return True

    @staticmethod
    async def init() -> DockerService:
        service = DockerService()

        if not await service.login_to_registry():
            raise SystemExit(
                f"Unable to log in to Docker registry '{settings.DOCKER_REGISTRY_URL}'. Exiting..."
            )
        ContainerPlatformBase.set_service(service)
        return service
