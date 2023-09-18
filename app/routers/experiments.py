from typing import Any

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from pydantic import Json

from app.authentication import get_current_user
from app.config import settings
from app.helpers import Pagination, eee_client_wrapper
from app.models.experiment import Experiment
from app.routers.aiod import get_dataset_name, get_model_name
from app.schemas.experiment import (
    ExperimentCreate,
    ExperimentResponse,
    ExperimentRun,
    ExperimentRunDetails,
    ExperimentRunExecute,
    ExperimentType,
)

router = APIRouter()


@router.get(
    "/experiments",
    response_model=list[ExperimentResponse],
)
async def get_experiments(pagination: Pagination = Depends()) -> Any:
    experiments = await Experiment.find_all(
        skip=pagination.offset, limit=pagination.limit
    ).to_list()
    return [experiment.dict() for experiment in experiments]


@router.get("/experiments/my", response_model=list[ExperimentResponse])
async def get_my_experiments(
    user: Json = Depends(get_current_user), pagination: Pagination = Depends()
) -> Any:
    experiments = await Experiment.find(
        Experiment.created_by == user["email"],
        skip=pagination.offset,
        limit=pagination.limit,
    ).to_list()
    return [experiment.dict() for experiment in experiments]


@router.get(
    "/count/experiments/my",
    response_model=int,
)
async def get_my_experiments_count(user: Json = Depends(get_current_user)) -> Any:
    number_of_my_experiments = await Experiment.find(
        Experiment.created_by == user["email"]
    ).count()
    return number_of_my_experiments


@router.get(
    "/count/experiments",
    response_model=int,
)
async def get_experiments_count() -> Any:
    return await Experiment.count()


@router.get(
    "/experiments/{id}",
    response_model=ExperimentResponse,
)
async def get_experiment(id: PydanticObjectId) -> Any:
    experiment = await Experiment.get(id)
    return experiment.dict()


@router.post(
    "/experiments",
    status_code=status.HTTP_201_CREATED,
    response_model=ExperimentResponse,
)
async def create_experiment(
    experiment: ExperimentCreate, user: Json = Depends(get_current_user)
) -> Any:
    experiment = Experiment(**experiment.dict(), created_by=user["email"])
    await experiment.create()
    return experiment.dict()


@router.get("/experiment/experiment-types", response_model=list[ExperimentType])
async def get_experiment_types(pagination: Pagination = Depends()) -> Any:
    async_client = eee_client_wrapper()
    res = await async_client.get(
        f"{settings.EEE_API.BASE_URL}/experiment-types?offset={pagination.offset}&limit={pagination.limit}",
    )

    if res.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=res.status_code,
            detail=f"Could not get experiment types from EEE API: {res.json()}",
        )

    return res.json()


@router.get("/experiment/experiment-types/{id}", response_model=ExperimentType)
async def get_experiment_type(id: PydanticObjectId) -> Any:
    async_client = eee_client_wrapper()
    res = await async_client.get(
        f"{settings.EEE_API.BASE_URL}/experiment-types/{id}",
    )

    if res.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=res.status_code,
            detail=f"Could not get experiment type from EEE API: {res.json()}",
        )

    return res.json()


@router.get("/experiments/{id}/runs", response_model=list[ExperimentRunDetails])
async def get_experiment_runs(
    id: PydanticObjectId, pagination: Pagination = Depends()
) -> Any:
    async_client = eee_client_wrapper()

    res = await async_client.get(
        f"{settings.EEE_API.BASE_URL}/experiment-runs?experiment_id={id}&"
        f"offset={pagination.offset}&limit={pagination.limit}",
    )

    return res.json()


@router.get("/experiment-runs/{id}", response_model=ExperimentRunDetails | None)
async def get_experiment_run(id: PydanticObjectId) -> Any:
    async_client = eee_client_wrapper()
    res = await async_client.get(
        f"{settings.EEE_API.BASE_URL}/experiment-runs/{id}",
    )

    return res.json()


@router.get("/experiment-runs/{id}/logs", response_class=PlainTextResponse)
async def get_experiment_run_logs(id: PydanticObjectId) -> str:
    async_client = eee_client_wrapper()
    res = await async_client.get(
        f"{settings.EEE_API.BASE_URL}/experiment-runs/{id}/logs",
    )

    if (text_response := res.json()) is not None:
        return text_response
    else:
        return ""


@router.post("/experiments/{id}/execute", response_model=ExperimentRun)
async def execute_experiment_run(id: PydanticObjectId, envs: dict[str, str]) -> Any:
    experiment = await Experiment.get(id)

    dataset_names = [await get_dataset_name(x) for x in experiment.dataset_ids]
    model_names = [await get_model_name(x) for x in experiment.model_ids]

    if any(x is None for x in dataset_names) or any(x is None for x in model_names):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    experiment_run = ExperimentRunExecute(
        id=experiment.id,
        experiment_type_id=experiment.experiment_type_id,
        dataset_names=dataset_names,
        model_names=model_names,
        env_vars=envs,
        metrics=experiment.metrics,
    )

    async_client = eee_client_wrapper()
    res = await async_client.post(
        f"{settings.EEE_API.BASE_URL}/experiment-runs", data=experiment_run.json()
    )

    if (
        res.status_code != status.HTTP_201_CREATED
        and res.status_code != status.HTTP_200_OK
    ):
        raise HTTPException(
            status_code=res.status_code,
            detail=f"Could not create experiment run in EEE API: {res.json()}",
        )

    return res.json()
