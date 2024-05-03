from datetime import datetime
from typing import Any

from beanie import PydanticObjectId, operators
from beanie.odm.queries.find import FindMany
from fastapi import APIRouter, Depends, HTTPException, status

from app.authentication import get_current_user
from app.config import settings
from app.helpers import Pagination, QueryOperator
from app.models.experiment_template import ExperimentTemplate
from app.schemas.experiment_template import (
    ExperimentTemplateCreate,
    ExperimentTemplateResponse,
)
from app.schemas.states import TemplateState
from app.services.experiment_scheduler import ExperimentScheduler

router = APIRouter()


@router.get("/experiment-templates", response_model=list[ExperimentTemplateResponse])
async def get_experiment_templates(
    user: dict = Depends(get_current_user(required=False)),
    pagination: Pagination = Depends(),
    only_mine: bool = False,
    include_pending: bool = False,
    only_finalized: bool = False,
) -> Any:
    result_set = find_specific_experiment_templates(
        only_mine=only_mine,
        include_pending=include_pending,
        only_finalized=only_finalized,
        query_operator=QueryOperator.AND,
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
    if experiment_template is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified experiment template doesn't exist",
        )
    return experiment_template.map_to_response()


@router.get("/count/experiment-templates", response_model=int)
async def get_experiment_templates_count(
    user: dict = Depends(get_current_user(required=False)),
    only_mine: bool = False,
    include_pending: bool = False,
    only_finalized: bool = False,
) -> Any:
    result_set = find_specific_experiment_templates(
        only_mine=only_mine,
        include_pending=include_pending,
        only_finalized=only_finalized,
        query_operator=QueryOperator.AND,
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
    user: dict = Depends(get_current_user(required=True)),
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
    is_approved: bool = False,
    exp_scheduler: ExperimentScheduler = Depends(ExperimentScheduler.get_service),
) -> Any:
    if password != settings.PASSWORD_FOR_TEMPLATE_APPROVAL:
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

    experiment_template.approved = is_approved
    experiment_template.updated_at = datetime.utcnow()

    await ExperimentTemplate.replace(experiment_template)
    await exp_scheduler.add_image_to_build(experiment_template.id)


def find_specific_experiment_templates(
    only_mine: bool,
    include_pending: bool,
    only_finalized: bool,
    query_operator: QueryOperator,
    user: dict | None,
    pagination: Pagination = None,
) -> FindMany[ExperimentTemplate]:
    search_conditions = []
    page_kwargs = (
        {"skip": pagination.offset, "limit": pagination.limit}
        if pagination is not None
        else {}
    )

    if user is None:
        if only_mine or include_pending:
            # Authentication required to see your experiment templates or pending experiment templates
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This endpoint requires authorization. You need to be logged in.",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        if only_mine:
            search_conditions.append(ExperimentTemplate.created_by == user["email"])

    if not include_pending:
        search_conditions.append(ExperimentTemplate.approved == True)  # noqa: E712
    if only_finalized:
        search_conditions.append(ExperimentTemplate.state == TemplateState.FINISHED)

    if len(search_conditions) > 0:
        multi_query = (
            operators.Or(*search_conditions)
            if query_operator == QueryOperator.OR
            else operators.And(*search_conditions)
        )
        return ExperimentTemplate.find(multi_query, **page_kwargs)

    return ExperimentTemplate.find_all(**page_kwargs)
