from pathlib import Path
from typing import Annotated, Any

from beanie import PydanticObjectId, operators
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse, StreamingResponse

from app.authentication import get_current_user
from app.config import TEMP_DIRNAME
from app.helpers import FileDetail, Pagination
from app.models.experiment import Experiment
from app.models.experiment_run import ExperimentRun
from app.schemas.experiment import ExperimentCreate, ExperimentResponse
from app.schemas.experiment_run import ExperimentRunDetails, ExperimentRunResponse
from app.services.experiment_scheduler import ExperimentScheduler
from app.services.workflow_engines.base import WorkflowEngineBase
from app.services.workflow_engines.reana import ReanaService

router = APIRouter()


@router.get(
    "/experiments",
    response_model=list[ExperimentResponse],
)
async def get_experiments(
    user: Annotated[dict, Depends(get_current_user(required=True))],
    pagination: Pagination = Depends(),
) -> Any:
    # TODO hotfix for returning only my experiments
    if user:
        experiments = await Experiment.find(
            Experiment.created_by == user["email"],
            skip=pagination.offset,
            limit=pagination.limit,
        ).to_list()
    else:
        experiments = []

    return [experiment.dict() for experiment in experiments]


@router.get(
    "/count/experiments",
    response_model=int,
)
async def get_experiments_count(
    user: Annotated[dict, Depends(get_current_user(required=True))],
) -> Any:
    # TODO hotfix for returning only my experiments
    if user:
        return await Experiment.find(Experiment.created_by == user["email"]).count()
    else:
        return 0


@router.get(
    "/experiments/{id}",
    response_model=ExperimentResponse,
)
async def get_experiment(
    id: PydanticObjectId,
    user: Annotated[dict, Depends(get_current_user(required=True))],
) -> Any:
    experiment = await Experiment.get(id)

    if experiment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified experiment doesn't exist",
        )

    await check_experiment_access_or_raise(id, user)
    return experiment.dict()


@router.post(
    "/experiments",
    status_code=status.HTTP_201_CREATED,
    response_model=ExperimentResponse,
)
async def create_experiment(
    experiment: ExperimentCreate,
    user: Annotated[dict, Depends(get_current_user(required=True))],
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
    user: dict = Depends(get_current_user(required=True)),
    exp_scheduler: ExperimentScheduler = Depends(ExperimentScheduler.get_service),
    workflow_engine: WorkflowEngineBase = Depends(WorkflowEngineBase.get_service),
) -> Any:
    experiment = await Experiment.get(id)

    if experiment is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Such experiment doesn't exist",
        )
    if not await experiment.uses_finished_template():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ExperimentTemplate of this experiment is yet to be finished",
        )
    if experiment.created_by != user["email"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You cannot execute experiments of other users.",
        )
    if not await workflow_engine.is_available():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Workflow engine is currently unavailable",
        )

    experiment_run = ExperimentRun(experiment_id=experiment.id)
    experiment_run = await experiment_run.create()

    await exp_scheduler.add_run_to_execute(experiment_run.id)
    return experiment_run.map_to_response()


@router.get("/experiments/{id}/runs", response_model=list[ExperimentRunResponse])
async def get_experiment_runs(
    id: PydanticObjectId,
    pagination: Pagination = Depends(),
    user: dict = Depends(get_current_user(required=True)),
) -> Any:
    await check_experiment_access_or_raise(id, user)

    runs = await ExperimentRun.find(
        ExperimentRun.experiment_id == id,
        skip=pagination.offset,
        limit=pagination.limit,
    ).to_list()

    return [run.map_to_response() for run in runs]


@router.get("/count/experiments/{id}/runs", response_model=int)
async def get_experiment_runs_count(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=True)),
) -> Any:
    await check_experiment_access_or_raise(id, user)
    return await ExperimentRun.find(ExperimentRun.experiment_id == id).count()


@router.get("/experiment-runs", response_model=list[ExperimentRunResponse])
async def get_all_experiment_runs(
    pagination: Pagination = Depends(),
    user: dict = Depends(get_current_user(required=True)),
) -> Any:
    # TODO hotfix for returning only my experiments
    my_experiments = await Experiment.find(
        Experiment.created_by == user["email"]
    ).to_list()
    if len(my_experiments) == 0:
        return []

    search_conditions = [
        ExperimentRun.experiment_id == exp.id for exp in my_experiments
    ]
    query = operators.Or(*search_conditions)

    runs = await ExperimentRun.find(
        query, skip=pagination.offset, limit=pagination.limit
    ).to_list()

    return [run.map_to_response() for run in runs]


@router.get("/experiment-runs/{id}", response_model=ExperimentRunDetails | None)
async def get_experiment_run(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=True)),
) -> Any:
    experiment_run = await ExperimentRun.get(id)

    if experiment_run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified experiment run doesn't exist",
        )

    await check_experiment_access_or_raise(experiment_run.experiment_id, user)
    return experiment_run.map_to_detailed_response()


@router.get("/experiment-runs/{id}/logs", response_class=PlainTextResponse)
async def get_experiment_run_logs(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=True)),
) -> str:
    experiment_run = await ExperimentRun.get(id)

    if experiment_run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified experiment run doesn't exist",
        )

    await check_experiment_access_or_raise(experiment_run.experiment_id, user)
    return experiment_run.logs


@router.get("/experiment-runs/{id}/files/download", response_class=StreamingResponse)
async def download_file(
    id: PydanticObjectId,
    filepath: str,
    workflow_engine: WorkflowEngineBase = Depends(ReanaService.get_service),
    user: dict = Depends(get_current_user(required=True)),
) -> bytes:
    experiment_run = await ExperimentRun.get(id)
    if experiment_run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified experiment run doesn't exist",
        )

    await check_experiment_access_or_raise(experiment_run.experiment_id, user)

    # TODO use temporaryFile/Directory package for this?
    tempdir = Path(TEMP_DIRNAME)
    tempdir.mkdir(parents=True, exist_ok=True)

    savepath = await workflow_engine.download_file(
        experiment_run, filepath, savedir=tempdir
    )
    if savepath is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Requested file doesn't exist.",
        )

    def iterfile():
        with open(savepath, "rb") as f:
            CHUNK_SIZE = 1024**2  # 1MB
            while chunk := f.read(CHUNK_SIZE):
                yield chunk
        savepath.unlink()

    headers = {"Content-Disposition": f'attachment; filename="{savepath.name}"'}
    return StreamingResponse(
        iterfile(), headers=headers, media_type="application/octet-stream"
    )


@router.get("/experiment-runs/{id}/files/list", response_model=list[FileDetail])
async def list_files(
    id: PydanticObjectId,
    workflow_engine: WorkflowEngineBase = Depends(ReanaService.get_service),
    user: dict = Depends(get_current_user(required=True)),
) -> list[FileDetail]:
    experiment_run = await ExperimentRun.get(id)
    if experiment_run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified experiment run doesn't exist",
        )

    await check_experiment_access_or_raise(experiment_run.experiment_id, user)
    return await workflow_engine.list_files(experiment_run)


async def check_experiment_access_or_raise(
    experiment_id: PydanticObjectId, user: dict | None
):
    experiment = await Experiment.get(experiment_id)

    # TODO: Add experiment access management
    if user is None or experiment.created_by != user["email"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You cannot access this experiment.",
        )
