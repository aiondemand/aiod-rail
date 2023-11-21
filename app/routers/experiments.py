from typing import Any

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from pydantic import Json

from app.authentication import get_current_user
from app.helpers import Pagination
from app.models.experiment import Experiment
from app.models.experiment_run import ExperimentRun
from app.schemas.experiment import ExperimentCreate, ExperimentResponse
from app.schemas.experiment_run import ExperimentRunDetails, ExperimentRunResponse
from app.services.experiment import ExperimentService

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
    "/count/experiments",
    response_model=int,
)
async def get_experiments_count() -> Any:
    return await Experiment.count()


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
    if not await experiment.is_valid():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Experiment request does not match its ExperimentTemplate",
        )

    await experiment.create()
    return experiment.dict()


@router.get("/experiments/{id}/execute", response_model=ExperimentRunResponse)
async def execute_experiment_run(
    id: PydanticObjectId,
    docker_service: ExperimentService = Depends(ExperimentService.get_docker_service),
) -> Any:
    experiment = await Experiment.get(id)

    if not await experiment.uses_finished_template():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ExperimentTemplate of this experiment is yet to be finished",
        )

    prev_experiment_runs = await ExperimentRun.find_many(
        ExperimentRun.experiment_id == experiment.id
    ).to_list()

    experiment_run = ExperimentRun(
        experiment_id=experiment.id,
        run_number=len(prev_experiment_runs),
    )
    experiment_run = await experiment_run.create()

    await docker_service.add_run_to_execute(experiment_run.id)

    return experiment_run.dict()


@router.get("/experiments/{id}/runs", response_model=list[ExperimentRunResponse])
async def get_experiment_runs(
    id: PydanticObjectId, pagination: Pagination = Depends()
) -> Any:
    runs = await ExperimentRun.find(
        ExperimentRun.experiment_id == id,
        skip=pagination.offset,
        limit=pagination.limit,
    ).to_list()

    return [run.dict() for run in runs]


@router.get("/experiment-runs", response_model=list[ExperimentRunResponse])
async def get_all_experiment_runs(pagination: Pagination = Depends()) -> Any:
    runs = await ExperimentRun.find_all(
        skip=pagination.offset, limit=pagination.limit
    ).to_list()
    return [run.dict() for run in runs]


@router.get("/experiment-runs/{id}", response_model=ExperimentRunDetails | None)
async def get_experiment_run(id: PydanticObjectId) -> Any:
    experiment_run = await ExperimentRun.get(id)
    return experiment_run.map_to_response()


@router.get("/experiment-runs/{id}/logs", response_class=PlainTextResponse)
async def get_experiment_run_logs(id: PydanticObjectId) -> str:
    # TODO
    raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Method not implemented"
    )
