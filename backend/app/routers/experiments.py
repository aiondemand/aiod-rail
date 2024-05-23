from typing import Any

from beanie import PydanticObjectId, operators
from beanie.odm.operators.find.comparison import Eq
from beanie.odm.operators.find.evaluation import Text
from beanie.odm.queries.find import FindMany
from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import get_current_user
from app.helpers import Pagination, QueryOperator, get_compare_operator_fn
from app.models.experiment import Experiment
from app.models.experiment_run import ExperimentRun
from app.models.experiment_template import ExperimentTemplate
from app.routers.experiment_templates import (
    get_experiment_template_if_accessible_or_raise,
)
from app.schemas.experiment import ExperimentCreate, ExperimentResponse
from app.services.workflow_engines.base import WorkflowEngineBase
from app.services.workflow_engines.reana import ReanaService

router = APIRouter()


@router.get("/experiments", response_model=list[ExperimentResponse])
async def get_experiments(
    query: str = "",
    user: dict = Depends(get_current_user(required=False)),
    pagination: Pagination = Depends(),
    mine: bool | None = None,
    archived: bool | None = None,
    public: bool | None = None,
) -> Any:
    result_set = find_specific_experiments(
        query,
        mine=mine,
        archived=archived,
        public=public,
        user=user,
        pagination=pagination,
    )
    experiments = await result_set.to_list()

    return [exp.map_to_response(user) for exp in experiments]


@router.get("/count/experiments", response_model=int)
async def get_experiments_count(
    query: str = "",
    user: dict = Depends(get_current_user(required=False)),
    mine: bool | None = None,
    archived: bool | None = None,
    public: bool | None = None,
) -> Any:
    result_set = find_specific_experiments(
        query,
        mine=mine,
        archived=archived,
        public=public,
        user=user,
    )
    return await result_set.count()


@router.get("/experiments/{id}", response_model=ExperimentResponse)
async def get_experiment(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=False)),
) -> Any:
    experiment = await get_experiment_if_accessible_or_raise(id, user)
    return experiment.map_to_response(user)


@router.post(
    "/experiments",
    status_code=status.HTTP_201_CREATED,
    response_model=ExperimentResponse,
)
async def create_experiment(
    experiment: ExperimentCreate,
    user: dict = Depends(get_current_user(required=True)),
) -> Any:
    template: ExperimentTemplate = await get_experiment_template_if_accessible_or_raise(
        experiment.experiment_template_id, user, write_access=False
    )
    if template.allows_experiment_creation is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Experiment template",
        )

    experiment_obj = Experiment(**experiment.dict(), created_by=user["email"])
    if not await experiment_obj.is_valid(template):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Experiment request does not match its ExperimentTemplate",
        )

    await experiment_obj.create()
    return experiment_obj.map_to_response(user)


@router.put("/experiments/{id}", response_model=ExperimentResponse)
async def update_experiment(
    id: PydanticObjectId,
    experiment: ExperimentCreate,
    user: dict = Depends(get_current_user(required=True)),
) -> Any:
    original_experiment = await get_experiment_if_accessible_or_raise(
        id, user, write_access=True
    )
    has_experiment_runs = (
        await ExperimentRun.find(ExperimentRun.experiment_id == id).count() > 0
    )

    experiment_to_save = await Experiment.update_experiment(
        original_experiment, experiment, editable_assets=has_experiment_runs is False
    )
    if experiment_to_save is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Performed changes to the experiment are not allowed",
        )

    await Experiment.replace(experiment_to_save)
    return experiment_to_save.map_to_response(user)


@router.delete("/experiments/{id}", response_model=None)
async def delete_experiment(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=True)),
    workflow_engine: WorkflowEngineBase = Depends(ReanaService.get_service),
) -> Any:
    await get_experiment_if_accessible_or_raise(id, user, write_access=True)

    runs = await ExperimentRun.find(ExperimentRun.experiment_id == id).to_list()
    for run in runs:
        await delete_run(run, workflow_engine)

    await Experiment.find(Experiment.id == id).delete()


@router.patch("/experiments/{id}/archive", response_model=None)
async def archive_experiment(
    id: PydanticObjectId,
    archived: bool = False,
    user: dict = Depends(get_current_user(required=True)),
) -> Any:
    experiment = await get_experiment_if_accessible_or_raise(
        id, user, write_access=True
    )
    experiment.archived = archived

    await Experiment.replace(experiment)


def find_specific_experiments(
    search_query: str,
    mine: bool | None,
    archived: bool | None,
    public: bool | None,
    user: dict | None,
    query_operator: QueryOperator = QueryOperator.AND,
    pagination: Pagination = None,
) -> FindMany[Experiment]:
    page_kwargs = (
        {"skip": pagination.offset, "limit": pagination.limit}
        if pagination is not None
        else {}
    )
    # initial condition -> retrieve only those objects that are accessible to a user
    accessibility_condition = operators.Or(
        ExperimentTemplate.public == True,  # noqa: E712
        Eq(ExperimentTemplate.created_by, user["email"] if user is not None else ""),
    )

    # applying filters
    filter_conditions = []
    if len(search_query) > 0:
        filter_conditions.append(Text(search_query))
    if mine is not None:
        if user is not None:
            filter_conditions.append(
                get_compare_operator_fn(mine)(Experiment.created_by, user["email"])
            )
        else:
            # Authentication required to see your experiment templates
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This endpoint requires authorization. You need to be logged in.",
                headers={"WWW-Authenticate": "Bearer"},
            )
    if archived:
        filter_conditions.append(Experiment.archived == archived)  # noqa: E712
    if public:
        filter_conditions.append(Experiment.public == public)  # noqa: E712

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
        status_code=status.HTTP_404_NOT_FOUND,
        detail="You cannot access this experiment",
    )
    experiment = await Experiment.get(experiment_id)

    if experiment is None:
        raise access_denied_error
    else:
        # Public experiments are readable by everyone
        if write_access is False and experiment.public:
            return experiment
        # TODO: Add experiment access management
        elif user is not None and experiment.created_by == user["email"]:
            return experiment
        else:
            raise access_denied_error


# TODO for now we shall put this function here to avoid circular imports
# TODO later add 'user' and 'public' attributes to experiment run so
# that we dont need to check these properties via retrieving the experiment
# they executed
# TODO this may also result in dependencies being less intertwined between routers
# TODO Ideally we dont want to call any logic/functions from this router to
# routers/experiment_runs.py file
async def delete_run(run: ExperimentRun, workflow_engine: WorkflowEngineBase) -> None:
    await workflow_engine.delete_workflow(run)
    await ExperimentRun.find(ExperimentRun.id == run.id).delete()
    await run.delete_files()
