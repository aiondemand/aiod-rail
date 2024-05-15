from pathlib import Path
from typing import Any

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse, StreamingResponse

from app.authentication import get_current_user
from app.config import TEMP_DIRNAME
from app.helpers import FileDetail, Pagination
from app.models.experiment_run import ExperimentRun
from app.routers.experiments import get_experiment_if_accessible_or_raise
from app.schemas.experiment_run import ExperimentRunDetails, ExperimentRunResponse
from app.services.experiment_scheduler import ExperimentScheduler
from app.services.workflow_engines.base import WorkflowEngineBase
from app.services.workflow_engines.reana import ReanaService

router = APIRouter()


@router.get("/experiments/{id}/execute", response_model=ExperimentRunResponse)
async def execute_experiment_run(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=True)),
    exp_scheduler: ExperimentScheduler = Depends(ExperimentScheduler.get_service),
    workflow_engine: WorkflowEngineBase = Depends(WorkflowEngineBase.get_service),
) -> Any:
    experiment = await get_experiment_if_accessible_or_raise(
        id, user, write_access=True
    )
    if experiment.is_usable is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid experiment to execute",
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
async def get_experiment_runs_of_experiment(
    id: PydanticObjectId,
    pagination: Pagination = Depends(),
    user: dict = Depends(get_current_user(required=False)),
) -> Any:
    await get_experiment_if_accessible_or_raise(id, user)

    runs = await ExperimentRun.find(
        ExperimentRun.experiment_id == id,
        skip=pagination.offset,
        limit=pagination.limit,
    ).to_list()

    return [run.map_to_response() for run in runs]


@router.get("/count/experiments/{id}/runs", response_model=int)
async def get_experiment_runs_of_experiment_count(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=False)),
) -> Any:
    await get_experiment_if_accessible_or_raise(id, user)
    return await ExperimentRun.find(ExperimentRun.experiment_id == id).count()


@router.get("/experiment-runs/{id}", response_model=ExperimentRunDetails | None)
async def get_experiment_run(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=False)),
) -> Any:
    experiment_run = await get_experiment_run_if_accessible_or_raise(id, user)
    return experiment_run.map_to_response(return_detailed_response=True)


@router.get("/experiment-runs/{id}/logs", response_class=PlainTextResponse)
async def get_experiment_run_logs(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=True)),
) -> str:
    experiment_run = await get_experiment_run_if_accessible_or_raise(id, user)
    return experiment_run.logs


@router.get("/experiment-runs/{id}/files/download", response_class=StreamingResponse)
async def download_file_from_experiment_run(
    id: PydanticObjectId,
    filepath: str,
    workflow_engine: WorkflowEngineBase = Depends(ReanaService.get_service),
    user: dict = Depends(get_current_user(required=True)),
) -> bytes:
    experiment_run = await get_experiment_run_if_accessible_or_raise(id, user)

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
async def list_files_of_experiment_run(
    id: PydanticObjectId,
    workflow_engine: WorkflowEngineBase = Depends(ReanaService.get_service),
    user: dict = Depends(get_current_user(required=True)),
) -> list[FileDetail]:
    experiment_run = await get_experiment_run_if_accessible_or_raise(id, user)
    return await workflow_engine.list_files(experiment_run)


async def get_experiment_run_if_accessible_or_raise(
    run_id: PydanticObjectId, user: dict | None
) -> ExperimentRun:
    experiment_run = await ExperimentRun.get(run_id)
    if experiment_run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified experiment run doesn't exist",
        )

    await get_experiment_if_accessible_or_raise(
        experiment_run.experiment_id, user, write_access=False
    )
    return experiment_run
