from datetime import datetime
from typing import Any

from beanie import PydanticObjectId, operators
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import Json

from app.authentication import get_current_user
from app.config import TRUE, settings
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


@router.get(
    "/experiment-templates/approved", response_model=list[ExperimentTemplateResponse]
)
async def get_approved_templates(pagination: Pagination = Depends()) -> Any:
    experiment_templates = await ExperimentTemplate.find(
        ExperimentTemplate.approved == TRUE,
        skip=pagination.offset,
        limit=pagination.limit,
    ).to_list()

    return [
        experiment_template.map_to_response()
        for experiment_template in experiment_templates
    ]


@router.get("/experiment-templates/my", response_model=list[ExperimentTemplateResponse])
async def get_my_experiment_templates(
    user: Json = Depends(get_current_user), pagination: Pagination = Depends()
) -> Any:
    experiment_templates = await ExperimentTemplate.find(
        ExperimentTemplate.created_by == user["email"],
        skip=pagination.offset,
        limit=pagination.limit,
    ).to_list()

    return [
        experiment_template.map_to_response()
        for experiment_template in experiment_templates
    ]


@router.get(
    "/experiment-templates/all-view", response_model=list[ExperimentTemplateResponse]
)
async def get_experiment_templates_all_view(
    user: Json = Depends(get_current_user), pagination: Pagination = Depends()
) -> Any:
    """
    a custom view of experiment templates that returns
    all approved templates and all current user templates
    """
    search_query = operators.Or(
        ExperimentTemplate.approved == TRUE,
        ExperimentTemplate.created_by == user["email"],
    )
    experiment_templates = await ExperimentTemplate.find(
        search_query, skip=pagination.offset, limit=pagination.limit
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


@router.get("/count/experiment-templates/approved", response_model=int)
async def get_approved_experiment_templates_count() -> Any:
    num_templates = await ExperimentTemplate.find(
        ExperimentTemplate.approved == TRUE
    ).count()
    return num_templates


@router.get("/count/experiment-templates/my", response_model=int)
async def get_my_experiment_templates_count(
    user: Json = Depends(get_current_user),
) -> Any:
    num_templates = await ExperimentTemplate.find(
        ExperimentTemplate.created_by == user["email"]
    ).count()
    return num_templates


@router.get("/count/experiment-templates/all-view", response_model=int)
async def get_experiment_templates_all_view_count(
    user: Json = Depends(get_current_user),
) -> Any:
    search_query = operators.Or(
        ExperimentTemplate.approved == TRUE,
        ExperimentTemplate.created_by == user["email"],
    )
    num_templates = await ExperimentTemplate.find(search_query).count()
    return num_templates


@router.post(
    "/experiment-templates",
    status_code=status.HTTP_201_CREATED,
    response_model=ExperimentTemplateResponse,
)
async def create_experiment_template(
    experiment_template_req: ExperimentTemplateCreate,
    user: Json = Depends(get_current_user),
) -> Any:
    experiment_template = ExperimentTemplate(
        **experiment_template_req.dict(), created_by=user["email"]
    )
    experiment_template = await experiment_template.create()

    experiment_template.initialize_files(
        dockerfile=experiment_template_req.dockerfile,
        pip_requirements=experiment_template_req.pip_requirements,
        script=experiment_template_req.script,
    )
    return experiment_template.map_to_response()


@router.patch("/experiment-templates/{id}/approve", response_model=None)
async def approve_experiment_template(
    id: PydanticObjectId,
    password: str,
    approve_value: bool = True,
    docker_service: ExperimentService = Depends(ExperimentService.get_docker_service),
) -> Any:
    if password != settings.PASSWORD_FOR_APPROVAL:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong password given",
        )

    experiment_template = await ExperimentTemplate.get(id)
    if experiment_template is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Such experiment template doesn't exist",
        )

    experiment_template.approved = approve_value
    experiment_template.updated_at = datetime.utcnow()

    await ExperimentTemplate.replace(experiment_template)
    await docker_service.add_image_to_build(experiment_template.id)
