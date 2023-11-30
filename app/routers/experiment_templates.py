from typing import Any

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, status

from app.helpers import Pagination
from app.models.experiment_template import ExperimentTemplate
from app.schemas.experiment_template import (
    ExperimentTemplateCreate,
    ExperimentTemplateResponse,
)
from app.services.experiment import ExperimentService

router = APIRouter()


@router.get("/experiment-templates", response_model=list[ExperimentTemplateResponse])
async def get_experiment_templates(pagination: Pagination = Depends()) -> Any:
    experiment_templates = await ExperimentTemplate.find_all(
        skip=pagination.offset, limit=pagination.limit
    ).to_list()

    return [
        experiment_template.map_to_response()
        for experiment_template in experiment_templates
    ]


@router.get("/experiment-templates/{id}", response_model=ExperimentTemplateResponse)
async def get_experiment_template(id: PydanticObjectId) -> Any:
    experiment_template = await ExperimentTemplate.get(id)
    return experiment_template.map_to_response()


@router.get("/count/experiment-templates", response_model=int)
async def get_experiment_templates_count() -> Any:
    return await ExperimentTemplate.count()


@router.post(
    "/experiment-templates",
    status_code=status.HTTP_201_CREATED,
    response_model=ExperimentTemplateResponse,
)
async def create_experiment_template(
    experiment_template_req: ExperimentTemplateCreate,
    docker_service: ExperimentService = Depends(ExperimentService.get_docker_service),
) -> Any:
    experiment_template = ExperimentTemplate(**experiment_template_req.dict())
    experiment_template = await experiment_template.create()

    experiment_template.initialize_files(
        dockerfile=experiment_template_req.dockerfile,
        pip_requirements=experiment_template_req.pip_requirements,
        script=experiment_template_req.script,
    )

    await docker_service.add_image_to_build(experiment_template.id)
    return experiment_template.map_to_response()
