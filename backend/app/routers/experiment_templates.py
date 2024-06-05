import shutil
from datetime import datetime, timezone
from typing import Any

from beanie import PydanticObjectId, operators
from beanie.odm.queries.find import FindMany
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.auth import get_current_user, raise_requires_auth
from app.config import settings
from app.helpers import Pagination, QueryOperator, get_compare_operator_fn
from app.models.experiment import Experiment
from app.models.experiment_template import ExperimentTemplate
from app.schemas.experiment_template import (
    ExperimentTemplateCreate,
    ExperimentTemplateResponse,
)
from app.schemas.states import TemplateState

router = APIRouter()


class ExperimentTemplateFilter(BaseModel):
    mine: bool | None = None
    archived: bool | None = None
    public: bool | None = None
    finalized: bool | None = None
    approved: bool | None = None


@router.get("/experiment-templates", response_model=list[ExperimentTemplateResponse])
async def get_experiment_templates(
    user: dict = Depends(get_current_user(required=False, from_api_key=True)),
    query: str = "",
    pagination: Pagination = Depends(),
    filters: ExperimentTemplateFilter = Depends(),
) -> Any:
    result_set = find_specific_experiment_templates(
        query,
        filters=filters,
        user=user,
        pagination=pagination,
    )
    experiment_templates = await result_set.to_list()

    return [
        experiment_template.map_to_response(user)
        for experiment_template in experiment_templates
    ]


@router.get("/experiment-templates/{id}", response_model=ExperimentTemplateResponse)
async def get_experiment_template(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=False, from_api_key=True)),
) -> Any:
    experiment_template = await get_experiment_template_if_accessible_or_raise(id, user)
    return experiment_template.map_to_response(user)


@router.get("/count/experiment-templates", response_model=int)
async def get_experiment_templates_count(
    user: dict = Depends(get_current_user(required=False, from_api_key=True)),
    query: str = "",
    filters: ExperimentTemplateFilter = Depends(),
) -> Any:
    result_set = find_specific_experiment_templates(
        query,
        filters=filters,
        user=user,
    )
    return await result_set.count()


@router.post(
    "/experiment-templates",
    status_code=status.HTTP_201_CREATED,
    response_model=ExperimentTemplateResponse,
)
async def create_experiment_template(
    experiment_template: ExperimentTemplateCreate,
    user: dict = Depends(get_current_user(required=True, from_api_key=True)),
) -> Any:
    experiment_template_obj = ExperimentTemplate(
        **experiment_template.dict(), created_by=user["email"]
    )
    if experiment_template_obj.is_valid() is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Experiment Template",
        )

    experiment_template_obj = await experiment_template_obj.create()
    experiment_template_obj.initialize_files(
        base_image=experiment_template.base_image,
        pip_requirements=experiment_template.pip_requirements,
        script=experiment_template.script,
    )
    return experiment_template_obj.map_to_response(user)


@router.put("/experiment-templates/{id}", response_model=ExperimentTemplateResponse)
async def update_experiment_template(
    id: PydanticObjectId,
    experiment_template: ExperimentTemplateCreate,
    user: dict = Depends(get_current_user(required=True, from_api_key=True)),
) -> Any:
    original_template = await get_experiment_template_if_accessible_or_raise(
        id, user, write_access=True
    )
    has_experiments = (
        await Experiment.find(Experiment.experiment_template_id == id).count() > 0
    )
    has_experiments_of_others = (
        await Experiment.find(
            Experiment.experiment_template_id == id,
            Experiment.created_by != user["email"],
        ).count()
        > 0
    )

    template_to_save = await ExperimentTemplate.update_template(
        original_template,
        experiment_template,
        editable_environment=has_experiments is False,
        editable_visibility=has_experiments_of_others is False,
    )
    if template_to_save is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Performed changes to the experiment template are not allowed",
        )

    await ExperimentTemplate.replace(template_to_save)
    return template_to_save.map_to_response(user)


@router.delete("/experiment-templates/{id}", response_model=None)
async def remove_experiment_template(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=True, from_api_key=True)),
) -> Any:
    await get_experiment_template_if_accessible_or_raise(id, user, write_access=True)
    exist_experiments = (
        await Experiment.find(Experiment.experiment_template_id == id).count() > 0
    )
    if exist_experiments:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This experiment template cannot be deleted.",
        )

    shutil.rmtree(settings.get_experiment_template_path(id))
    await ExperimentTemplate.find(ExperimentTemplate.id == id).delete()


@router.patch("/experiment-templates/{id}/archive", response_model=None)
async def archive_experiment_template(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=True, from_api_key=True)),
    archive: bool = False,
) -> Any:
    experiment_template = await get_experiment_template_if_accessible_or_raise(
        id, user, write_access=True
    )
    await experiment_template.set(
        {
            ExperimentTemplate.is_archived: archive,
            ExperimentTemplate.updated_at: datetime.now(tz=timezone.utc),
        }
    )


@router.get("/count/experiment-templates/{id}/experiments", response_model=int)
async def get_experiments_of_template_count(
    id: PydanticObjectId,
    only_mine: bool = False,
    user: dict = Depends(get_current_user(required=False, from_api_key=True)),
) -> Any:
    await get_experiment_template_if_accessible_or_raise(id, user)

    if user is None and only_mine:
        raise_requires_auth()

    search_conditions = [Experiment.created_by == user["email"]] if only_mine else []
    search_conditions.append(Experiment.experiment_template_id == id)

    return await Experiment.find(*search_conditions).count()


def find_specific_experiment_templates(
    search_query: str,
    filters: ExperimentTemplateFilter,
    user: dict | None,
    query_operator: QueryOperator = QueryOperator.AND,
    pagination: Pagination = None,
) -> FindMany[ExperimentTemplate]:
    page_kwargs = (
        {"skip": pagination.offset, "limit": pagination.limit}
        if pagination is not None
        else {}
    )

    # applying filters
    filter_conditions = []
    if len(search_query) > 0:
        filter_conditions.append(operators.Text(search_query))
    if filters.mine is not None:
        if user is not None:
            filter_conditions.append(
                get_compare_operator_fn(filters.mine)(
                    Experiment.created_by, user["email"]
                )
            )
        else:
            # Authentication required to see your experiment templates
            raise_requires_auth()

    if filters.finalized is not None:
        filter_conditions.append(
            get_compare_operator_fn(filters.finalized)(
                ExperimentTemplate.state, TemplateState.FINISHED
            )
        )
    if filters.approved is not None:
        filter_conditions.append(ExperimentTemplate.is_approved == filters.approved)
    if filters.archived is not None:
        filter_conditions.append(ExperimentTemplate.is_archived == filters.archived)
    if filters.public is not None:
        filter_conditions.append(ExperimentTemplate.is_public == filters.public)

    accessibility_condition = ExperimentTemplate.get_query_readable_by_user(user)

    if len(filter_conditions) > 0:
        filter_multi_query = (
            operators.Or(*filter_conditions)
            if query_operator == QueryOperator.OR
            else operators.And(*filter_conditions)
        )
        final_query = operators.And(accessibility_condition, filter_multi_query)
    else:
        final_query = accessibility_condition

    return ExperimentTemplate.find(final_query, **page_kwargs)


async def get_experiment_template_if_accessible_or_raise(
    template_id: PydanticObjectId, user: dict | None, write_access: bool = False
) -> ExperimentTemplate:
    access_denied_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You cannot access this experiment template",
    )
    template = await ExperimentTemplate.get(template_id)
    if template is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified experiment template doesn't exist",
        )

    if template is None:
        raise access_denied_error
    else:
        if write_access and template.is_editable_by_user(user):
            return template
        elif not write_access and template.is_readable_by_user(user):
            return template
        else:
            raise access_denied_error
