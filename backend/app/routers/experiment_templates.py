from datetime import datetime
from typing import Any

from beanie import PydanticObjectId, operators
from beanie.odm.queries.find import FindMany
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import Json

from app.authentication import get_current_user, get_current_user_optional
from app.config import settings
from app.helpers import Pagination, QueryOperator
from app.models.experiment_template import ExperimentTemplate
from app.schemas.experiment_template import (
    ExperimentTemplateCreate,
    ExperimentTemplateResponse,
)
from app.services.experiment import ExperimentService

router = APIRouter()


@router.get("/experiment-templates", response_model=list[ExperimentTemplateResponse])
async def get_experiment_templates(
    user: Json = Depends(get_current_user_optional),
    pagination: Pagination = Depends(),
    include_mine: bool = False,
    include_approved: bool = False,
    query_operator: QueryOperator = QueryOperator.AND,
) -> Any:
    result_set = find_specific_experiment_templates(
        include_mine=include_mine,
        include_approved=include_approved,
        query_operator=query_operator,
        user=user,
        pagination=pagination,
    )
    experiment_templates = await result_set.to_list()

    return [
        experiment_template.map_to_response()
        for experiment_template in experiment_templates
    ]


@router.get("/experiment-templates/{id}", response_model=ExperimentTemplateResponse)
async def get_experiment_template(id: PydanticObjectId) -> Any:
    experiment_template = await ExperimentTemplate.get(id)
    return experiment_template.map_to_response()


@router.get("/count/experiment-templates", response_model=int)
async def get_experiment_templates_count(
    user: Json = Depends(get_current_user_optional),
    include_mine: bool = False,
    include_approved: bool = False,
    query_operator: QueryOperator = QueryOperator.AND,
) -> Any:
    result_set = find_specific_experiment_templates(
        include_mine=include_mine,
        include_approved=include_approved,
        query_operator=query_operator,
        user=user,
    )
    return await result_set.count()


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
        base_image=experiment_template_req.base_image,
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


def find_specific_experiment_templates(
    include_mine: bool,
    include_approved: bool,
    query_operator: QueryOperator,
    user: Json,
    pagination: Pagination = None,
) -> FindMany[ExperimentTemplate]:
    search_condtions = []
    page_kwargs = (
        {"skip": pagination.offset, "limit": pagination.limit}
        if pagination is not None
        else {}
    )

    if len(user) == 0 and include_mine and not include_approved:
        # You need to be authorized to see only your experiment templates
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This endpoint requires authorization. You need to be logged in.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if len(user) == 0:
        include_mine = False
    if include_mine:
        search_condtions.append(ExperimentTemplate.created_by == user["email"])
    if include_approved:
        search_condtions.append(ExperimentTemplate.approved == True)  # noqa: E712

    if len(search_condtions) > 0:
        multi_query = (
            operators.Or(*search_condtions)
            if query_operator == QueryOperator.OR
            else operators.And(*search_condtions)
        )
        return ExperimentTemplate.find(multi_query, **page_kwargs)

    return ExperimentTemplate.find_all(**page_kwargs)
