from datetime import datetime, timezone
from functools import partial
from typing import Any, Awaitable, Callable

from beanie import PydanticObjectId, operators
from beanie.odm.queries.find import FindMany
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.auth import get_current_user, raise_requires_auth
from app.helpers import Pagination, QueryOperator, get_compare_operator_fn
from app.models.experiment import Experiment
from app.models.experiment_run import ExperimentRun
from app.routers.experiment_runs import delete_run, set_archived_run, set_public_run
from app.routers.experiment_templates import (
    get_experiment_template_if_accessible_or_raise,
)
from app.schemas.experiment import ExperimentCreate, ExperimentResponse
from app.schemas.experiment_run import ExperimentRunResponse
from app.services.experiment_scheduler import ExperimentScheduler
from app.services.workflow_engines.base import WorkflowEngineBase
from app.services.workflow_engines.reana import ReanaService

router = APIRouter()


class ExperimentFilter(BaseModel):
    mine: bool | None = None
    archived: bool | None = None
    public: bool | None = None


@router.get("/experiments", response_model=list[ExperimentResponse])
async def get_experiments(
    query: str = "",
    user: dict = Depends(get_current_user(required=False, from_api_key=True)),
    pagination: Pagination = Depends(),
    filters: ExperimentFilter = Depends(),
) -> Any:
    result_set = find_specific_experiments(
        query,
        filters=filters,
        user=user,
        pagination=pagination,
    )
    experiments = await result_set.to_list()

    return [exp.map_to_response(user) for exp in experiments]


@router.get("/count/experiments", response_model=int)
async def get_experiments_count(
    query: str = "",
    user: dict = Depends(get_current_user(required=False, from_api_key=True)),
    filters: ExperimentFilter = Depends(),
) -> Any:
    result_set = find_specific_experiments(
        query,
        filters=filters,
        user=user,
    )
    return await result_set.count()


@router.get("/experiments/{id}", response_model=ExperimentResponse)
async def get_experiment(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=False, from_api_key=True)),
) -> Any:
    experiment = await get_experiment_if_accessible_or_raise(id, user)
    return experiment.map_to_response(user)


@router.get("/experiments/{id}/runs", response_model=list[ExperimentRunResponse])
async def get_experiment_runs_of_experiment(
    id: PydanticObjectId,
    pagination: Pagination = Depends(),
    user: dict = Depends(get_current_user(required=False, from_api_key=True)),
) -> Any:
    await get_experiment_if_accessible_or_raise(id, user)

    runs = await ExperimentRun.find(
        ExperimentRun.experiment_id == id,
        skip=pagination.offset,
        limit=pagination.limit,
    ).to_list()

    return [run.map_to_response(user) for run in runs]


@router.get("/count/experiments/{id}/runs", response_model=int)
async def get_experiment_runs_of_experiment_count(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=False, from_api_key=True)),
) -> Any:
    await get_experiment_if_accessible_or_raise(id, user)
    return await ExperimentRun.find(ExperimentRun.experiment_id == id).count()


@router.post(
    "/experiments",
    status_code=status.HTTP_201_CREATED,
    response_model=ExperimentResponse,
)
async def create_experiment(
    experiment: ExperimentCreate,
    user: dict = Depends(get_current_user(required=True, from_api_key=True)),
) -> Any:
    template = await get_experiment_template_if_accessible_or_raise(
        experiment.experiment_template_id, user, write_access=False
    )
    if template.allows_experiment_creation is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Experiment template",
        )

    experiment_obj = await Experiment.create_experiment(
        experiment, template, user["email"]
    )
    if experiment_obj is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Experiment request does not match its ExperimentTemplate",
        )

    await experiment_obj.create()
    return experiment_obj.map_to_response(user)


@router.get("/experiments/{id}/execute", response_model=ExperimentRunResponse)
async def execute_experiment_run(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=True, from_api_key=True)),
    exp_scheduler: ExperimentScheduler = Depends(ExperimentScheduler.get_service),
    workflow_engine: WorkflowEngineBase = Depends(WorkflowEngineBase.get_service),
) -> Any:
    experiment = await get_experiment_if_accessible_or_raise(
        id, user, write_access=True
    )
    if experiment.allows_execution is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid experiment to execute",
        )
    if not await workflow_engine.is_available():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Workflow engine is currently unavailable",
        )

    experiment_run = ExperimentRun(
        experiment_id=experiment.id,
        created_by=user["email"],
        is_public=experiment.is_public,
    )
    experiment_run = await experiment_run.create()

    await exp_scheduler.add_run_to_execute(experiment_run.id)
    return experiment_run.map_to_response(user)


@router.put("/experiments/{id}", response_model=ExperimentResponse)
async def update_experiment(
    id: PydanticObjectId,
    experiment: ExperimentCreate,
    user: dict = Depends(get_current_user(required=True, from_api_key=True)),
) -> Any:
    original_experiment = await get_experiment_if_accessible_or_raise(
        id, user, write_access=True
    )
    runs = await ExperimentRun.find(ExperimentRun.experiment_id == id).to_list()
    template = await get_experiment_template_if_accessible_or_raise(
        experiment.experiment_template_id, user, write_access=False
    )
    has_experiment_runs = len(runs) > 0

    experiment_to_save = await Experiment.update_experiment(
        original_experiment,
        experiment,
        template,
        editable_assets=has_experiment_runs is False,
    )
    if experiment_to_save is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Performed changes to the experiment are not allowed",
        )

    await run_cascade_operation(
        runs,
        partial(
            set_public_run,
            value=experiment_to_save.is_public,
            updated_at=experiment_to_save.updated_at,
        ),
    )
    await Experiment.replace(experiment_to_save)
    return experiment_to_save.map_to_response(user)


@router.delete("/experiments/{id}", response_model=None)
async def delete_experiment(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=True, from_api_key=True)),
    workflow_engine: WorkflowEngineBase = Depends(ReanaService.get_service),
) -> Any:
    await get_experiment_if_accessible_or_raise(id, user, write_access=True)

    runs = await ExperimentRun.find(ExperimentRun.experiment_id == id).to_list()
    await run_cascade_operation(
        runs, partial(delete_run, workflow_engine=workflow_engine)
    )
    await Experiment.find(Experiment.id == id).delete()


@router.patch("/experiments/{id}/archive", response_model=None)
async def archive_experiment(
    id: PydanticObjectId,
    archive: bool = False,
    user: dict = Depends(get_current_user(required=True, from_api_key=True)),
) -> Any:
    experiment = await get_experiment_if_accessible_or_raise(
        id, user, write_access=True
    )
    updated_at = datetime.now(tz=timezone.utc)

    runs = await ExperimentRun.find(ExperimentRun.experiment_id == id).to_list()
    await run_cascade_operation(
        runs, partial(set_archived_run, value=archive, updated_at=updated_at)
    )

    await experiment.set(
        {Experiment.is_archived: archive, Experiment.updated_at: updated_at}
    )


def find_specific_experiments(
    search_query: str,
    filters: ExperimentFilter,
    user: dict | None,
    query_operator: QueryOperator = QueryOperator.AND,
    pagination: Pagination = None,
) -> FindMany[Experiment]:
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
    if filters.archived:
        filter_conditions.append(Experiment.is_archived == filters.archived)
    if filters.public:
        filter_conditions.append(Experiment.is_public == filters.public)

    accessibility_condition = Experiment.get_query_readable_by_user(user)

    if len(filter_conditions) > 0:
        filter_multi_query = (
            operators.Or(*filter_conditions)
            if query_operator == QueryOperator.OR
            else operators.And(*filter_conditions)
        )
        final_query = operators.And(accessibility_condition, filter_multi_query)
    else:
        final_query = accessibility_condition

    return Experiment.find(final_query, **page_kwargs)


async def get_experiment_if_accessible_or_raise(
    experiment_id: PydanticObjectId, user: dict | None, write_access: bool = False
) -> Experiment:
    access_denied_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You cannot access this experiment",
    )
    experiment = await Experiment.get(experiment_id)

    if experiment is None:
        raise access_denied_error
    else:
        if write_access and experiment.is_editable_by_user(user):
            return experiment
        elif not write_access and experiment.is_readable_by_user(user):
            return experiment
        else:
            raise access_denied_error


async def run_cascade_operation(
    runs: list[ExperimentRun], operation_fn: Callable[[ExperimentRun], Awaitable[None]]
) -> None:
    for run in runs:
        await operation_fn(run)
