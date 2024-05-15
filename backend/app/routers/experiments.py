from typing import Any

from beanie import PydanticObjectId, operators
from beanie.odm.operators.find.evaluation import Text
from beanie.odm.queries.find import FindMany
from fastapi import APIRouter, Depends, HTTPException, status

from app.authentication import get_current_user
from app.helpers import Pagination, QueryOperator
from app.models.experiment import Experiment
from app.models.experiment_run import ExperimentRun
from app.models.experiment_template import ExperimentTemplate
from app.routers.experiment_templates import (
    get_experiment_template_if_accessible_or_raise,
)
from app.schemas.experiment import ExperimentCreate, ExperimentResponse

router = APIRouter()


@router.get("/experiments", response_model=list[ExperimentResponse])
async def get_experiments(
    query: str = "",
    user: dict = Depends(get_current_user(required=False)),
    pagination: Pagination = Depends(),
    only_mine: bool = False,
    only_usable: bool = False,
    only_public: bool = False,
) -> Any:
    result_set = find_specific_experiments(
        query,
        only_mine=only_mine,
        only_usable=only_usable,
        only_public=only_public,
        query_operator=QueryOperator.AND,
        user=user,
        pagination=pagination,
    )
    experiments = await result_set.to_list()

    return [exp.map_to_response() for exp in experiments]


@router.get("/count/experiments", response_model=int)
async def get_experiments_count(
    query: str = "",
    user: dict = Depends(get_current_user(required=False)),
    only_mine: bool = False,
    only_usable: bool = False,
    only_public: bool = False,
) -> Any:
    result_set = find_specific_experiments(
        query,
        only_mine=only_mine,
        only_usable=only_usable,
        only_public=only_public,
        query_operator=QueryOperator.AND,
        user=user,
    )
    out = await result_set.count()  # TODO
    return out


@router.get("/experiments/{id}", response_model=ExperimentResponse)
async def get_experiment(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=False)),
) -> Any:
    experiment = await get_experiment_if_accessible_or_raise(id, user)
    return experiment.map_to_response()


@router.get("/experiments/{id}/is_editable", response_model=bool)
async def is_experiment_editable(
    id: PydanticObjectId, user: dict = Depends(get_current_user(required=False))
) -> Any:
    experiment = await Experiment.get(id)
    if experiment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified experiment doesn't exist",
        )

    return (
        user is not None
        and experiment.created_by == user["email"]
        and experiment.is_usable
    )


@router.post(
    "/experiments",
    status_code=status.HTTP_201_CREATED,
    response_model=ExperimentResponse,
)
async def create_experiment(
    experiment_req: ExperimentCreate,
    user: dict = Depends(get_current_user(required=True)),
) -> Any:
    template: ExperimentTemplate = await get_experiment_template_if_accessible_or_raise(
        experiment_req.experiment_template_id, user, write_access=False
    )
    if template.allows_experiment_creation is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Experiment template",
        )

    experiment = Experiment(**experiment_req.dict(), created_by=user["email"])
    if not await experiment.is_valid(template):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Experiment request does not match its ExperimentTemplate",
        )

    await experiment.create()
    return experiment.map_to_response()


@router.put("/experiments/{id}", response_model=ExperimentResponse)
async def update_experiment(
    id: PydanticObjectId,
    experiment_req: ExperimentCreate,
    user: dict = Depends(get_current_user(required=True)),
) -> Any:
    old_experiment = await get_experiment_if_accessible_or_raise(
        id, user, write_access=True
    )
    editable_assets = (
        await ExperimentRun.find(ExperimentRun.experiment_id == id).count() == 0
    )

    experiment_to_save = await Experiment.update_experiment(
        old_experiment, experiment_req, editable_assets
    )
    if experiment_to_save is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Performed changes to the experiment are not allowed",
        )

    await Experiment.replace(experiment_to_save)
    return experiment_to_save.map_to_response()


@router.delete("/experiments/{id}", response_model=None)
async def delete_experiment(
    id: PydanticObjectId, user: dict = Depends(get_current_user(required=True))
) -> Any:
    await get_experiment_if_accessible_or_raise(id, user, write_access=True)
    exist_runs = await ExperimentRun.find(ExperimentRun.experiment_id == id).count() > 0
    if exist_runs:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This experiment cannot be deleted",
        )

    await Experiment.find(Experiment.id == id).delete()


@router.patch("/experiments/{id}/usability", response_model=None)
async def set_experiment_usability(
    id: PydanticObjectId,
    is_usable: bool = True,
    user: dict = Depends(get_current_user(required=True)),
) -> Any:
    experiment = await get_experiment_if_accessible_or_raise(
        id, user, write_access=True
    )
    experiment.is_usable = is_usable

    await Experiment.replace(experiment)


def find_specific_experiments(
    search_query: str,
    only_mine: bool,
    only_usable: bool,
    only_public: bool,
    query_operator: QueryOperator,
    user: dict | None,
    pagination: Pagination = None,
) -> FindMany[Experiment]:
    search_conditions = []
    page_kwargs = (
        {"skip": pagination.offset, "limit": pagination.limit}
        if pagination is not None
        else {}
    )
    if len(search_query) > 0:
        search_conditions.append(Text(search_query))

    if user is None and only_mine:
        # Authentication required to see your experiments
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This endpoint requires authorization. You need to be logged in.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif only_mine:
        search_conditions.append(Experiment.created_by == user["email"])

    if only_usable:
        search_conditions.append(Experiment.is_usable == True)  # noqa: E712
    if only_public:
        search_conditions.append(Experiment.is_public == True)  # noqa: E712

    if len(search_conditions) > 0:
        multi_query = (
            operators.Or(*search_conditions)
            if query_operator == QueryOperator.OR
            else operators.And(*search_conditions)
        )
        return Experiment.find(multi_query, **page_kwargs)

    return Experiment.find_all(**page_kwargs)


async def get_experiment_if_accessible_or_raise(
    experiment_id: PydanticObjectId, user: dict | None, write_access: bool = False
) -> Experiment:
    experiment = await Experiment.get(experiment_id)
    if experiment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified experiment doesn't exist",
        )
    if write_access is False and experiment.is_public:
        return experiment

    # TODO: Add experiment access management
    if not user or experiment.created_by != user["email"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You cannot access this experiment.",
        )
    return experiment
