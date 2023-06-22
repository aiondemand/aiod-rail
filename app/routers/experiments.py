from typing import Any

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, status

from app.config import settings
from app.helpers import Pagination, eee_client_wrapper
from app.models.experiment import Experiment
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
async def create_experiment(experiment: ExperimentCreate) -> Any:
    experiment = Experiment(**experiment.dict())
    await experiment.create()
    return experiment.dict()


@router.get("/experiment/experiment-types", response_model=list[ExperimentType])
async def get_experiment_types(pagination: Pagination = Depends()) -> Any:
    async_client = eee_client_wrapper()
    res = await async_client.get(
        f"{settings.EEE_API.BASE_URL}/experiment-types?offset={pagination.offset}&limit={pagination.limit}",
    )
    return res.json()


@router.get("/experiments/{id}/runs", response_model=list[ExperimentRun])
async def get_experiment_runs(
    id: PydanticObjectId, pagination: Pagination = Depends()
) -> Any:
    async_client = eee_client_wrapper()

    res = await async_client.get(
        f"{settings.EEE_API.BASE_URL}/experiment-runs?experiment_id={id}&"
        f"offset={pagination.offset}&limit={pagination.limit}",
    )

    return res.json()


@router.get(
    "/experiments/{id}/runs/{run_id}", response_model=ExperimentRunDetails | None
)
async def get_experiment_run(id: PydanticObjectId, run_id: PydanticObjectId) -> Any:
    async_client = eee_client_wrapper()
    res = await async_client.get(
        f"{settings.EEE_API.BASE_URL}/experiment-runs/{run_id}",
    )

    return res.json()


@router.post("/experiments/{id}/execute", response_model=ExperimentRun)
async def execute_experiment_run(id: PydanticObjectId, envs: dict[str, str]) -> Any:
    experiment = await Experiment.get(id)
    experiment_run = ExperimentRunExecute(
        id=experiment.id,
        experiment_type_id=experiment.experiment_type_id,
        dataset_name="mtkinit/Example-Dataset-Super-2",
        model_name="j-hartmann/sentiment-roberta-large-english-3-classes",
        env_vars=envs,
        metrics=experiment.metrics,
    )

    async_client = eee_client_wrapper()
    res = await async_client.post(
        f"{settings.EEE_API.BASE_URL}/experiment-runs", data=experiment_run.json()
    )

    return res.json()
