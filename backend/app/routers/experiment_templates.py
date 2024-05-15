import shutil
from datetime import datetime, timezone
from typing import Any

from beanie import PydanticObjectId, operators
from beanie.odm.operators.find.evaluation import Text
from beanie.odm.queries.find import FindMany
from fastapi import APIRouter, Depends, HTTPException, status

from app.authentication import get_current_user
from app.config import settings
from app.helpers import Pagination, QueryOperator
from app.models.experiment import Experiment
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
    query: str = "",
    pagination: Pagination = Depends(),
    only_mine: bool = False,
    only_finalized: bool = False,
    only_usable: bool = False,
    only_public: bool = False,
) -> Any:
    result_set = find_specific_experiment_templates(
        query,
        only_mine=only_mine,
        only_finalized=only_finalized,
        only_usable=only_usable,
        only_public=only_public,
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
async def get_experiment_template(
    id: PydanticObjectId, user: dict = Depends(get_current_user(required=False))
) -> Any:
    experiment_template = await get_experiment_template_if_accessible_or_raise(id, user)
    return experiment_template.map_to_response()


@router.get("/experiment-templates/{id}/is_editable", response_model=bool)
async def is_experiment_template_editable(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=False)),
) -> Any:
    experiment_template = await ExperimentTemplate.get(id)
    if experiment_template is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified experiment template doesn't exist",
        )

    return (
        user is not None
        and experiment_template.created_by == user["email"]
        and experiment_template.is_usable
    )


@router.get("/count/experiment-templates", response_model=int)
async def get_experiment_templates_count(
    user: dict = Depends(get_current_user(required=False)),
    query: str = "",
    only_mine: bool = False,
    only_finalized: bool = False,
    only_usable: bool = False,
    only_public: bool = False,
) -> Any:
    result_set = find_specific_experiment_templates(
        query,
        only_mine=only_mine,
        only_finalized=only_finalized,
        only_usable=only_usable,
        only_public=only_public,
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


@router.put("/experiment-templates/{id}", response_model=ExperimentTemplateResponse)
async def update_experiment_template(
    id: PydanticObjectId,
    experiment_template_req: ExperimentTemplateCreate,
    user: dict = Depends(get_current_user(required=True)),
) -> Any:
    old_exp_template = await get_experiment_template_if_accessible_or_raise(
        id, user, write_access=True
    )
    editable_environment = (
        await Experiment.find(Experiment.experiment_template_id == id).count() == 0
    )
    editable_visibility = (
        await Experiment.find(
            Experiment.experiment_template_id == id,
            Experiment.created_by != user["email"],
        ).count()
        == 0
    )

    template_to_save = await ExperimentTemplate.update_template(
        old_exp_template,
        experiment_template_req,
        editable_environment,
        editable_visibility,
    )
    if template_to_save is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Performed changes to the experiment template are not allowed",
        )

    await ExperimentTemplate.replace(template_to_save)
    return template_to_save.map_to_response()


@router.delete("/experiment-templates/{id}", response_model=None)
async def remove_experiment_template(
    id: PydanticObjectId, user: dict = Depends(get_current_user(required=True))
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


@router.patch("/experiment-templates/{id}/usability", response_model=None)
async def set_experiment_template_usability(
    id: PydanticObjectId,
    is_usable: bool = True,
    user: dict = Depends(get_current_user(required=True)),
) -> Any:
    experiment_template = await get_experiment_template_if_accessible_or_raise(
        id, user, write_access=True
    )
    experiment_template.is_usable = is_usable

    await ExperimentTemplate.replace(experiment_template)


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

    experiment_template.is_approved = is_approved
    experiment_template.updated_at = datetime.now(tz=timezone.utc)
    await ExperimentTemplate.replace(experiment_template)

    if is_approved:
        await exp_scheduler.add_image_to_build(experiment_template.id)


@router.get("/count/experiment-templates/{id}/experiments", response_model=int)
async def get_experiments_of_template_count(
    id: PydanticObjectId,
    only_mine: bool = False,
    user: dict = Depends(get_current_user(required=True)),
) -> Any:
    await get_experiment_template_if_accessible_or_raise(id, user)

    search_conditions = [Experiment.created_by == user["email"]] if only_mine else []
    search_conditions.append(Experiment.experiment_template_id == id)

    return await Experiment.find(*search_conditions).count()


def find_specific_experiment_templates(
    search_query: str,
    only_mine: bool,
    only_finalized: bool,
    only_usable: bool,
    only_public: bool,
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
    if len(search_query) > 0:
        search_conditions.append(Text(search_query))

    if only_mine:
        if user is not None:
            search_conditions.append(ExperimentTemplate.created_by == user["email"])
        else:
            # Authentication required to see your experiment templates
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This endpoint requires authorization. You need to be logged in.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    if only_finalized:
        search_conditions.append(ExperimentTemplate.state == TemplateState.FINISHED)
    if only_usable:
        search_conditions.append(ExperimentTemplate.is_usable == True)  # noqa: E712
    if only_public:
        search_conditions.append(ExperimentTemplate.is_public == True)  # noqa: E712

    if len(search_conditions) > 0:
        multi_query = (
            operators.Or(*search_conditions)
            if query_operator == QueryOperator.OR
            else operators.And(*search_conditions)
        )
        return ExperimentTemplate.find(multi_query, **page_kwargs)

    return ExperimentTemplate.find_all(**page_kwargs)


async def get_experiment_template_if_accessible_or_raise(
    template_id: PydanticObjectId, user: dict | None, write_access: bool = False
) -> ExperimentTemplate:
    template = await ExperimentTemplate.get(template_id)
    if template is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified experiment template doesn't exist",
        )
    if write_access is False and template.is_public:
        return template

    # TODO: Add experiment access management
    if user is None or template.created_by != user["email"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You cannot access this experiment template.",
        )
    return template
