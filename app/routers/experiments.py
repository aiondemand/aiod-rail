from typing import Any

from beanie import PydanticObjectId
from fastapi import APIRouter, status

from app.config import settings
from app.models.experiment import Experiment
from app.schemas.experiment import ExperimentCreate, ExperimentResponse

router = APIRouter()


@router.get(
    "/experiments",
    response_model=list[ExperimentResponse],
)
async def get_experiments(
    offset: int = 0, limit: int = settings.DEFAULT_RESPONSE_LIMIT
) -> Any:
    experiments = await Experiment.find_all(skip=offset, limit=limit).to_list()
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
