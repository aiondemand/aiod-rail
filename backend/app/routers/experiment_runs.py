from pathlib import Path
from typing import Any

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse, StreamingResponse

from app.authentication import get_current_user
from app.config import TEMP_DIRNAME
from app.helpers import FileDetail, Pagination
from app.models.experiment import Experiment
from app.models.experiment_run import ExperimentRun
from app.routers.experiments import delete_run, get_experiment_if_accessible_or_raise
from app.schemas.experiment_run import ExperimentRunDetails, ExperimentRunResponse
from app.schemas.states import RunState
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
    if experiment.allows_experiment_execution is False:
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
    return experiment_run.map_to_response(mine=True)


@router.get("/experiments/{id}/runs", response_model=list[ExperimentRunResponse])
async def get_experiment_runs_of_experiment(
    id: PydanticObjectId,
    pagination: Pagination = Depends(),
    user: dict = Depends(get_current_user(required=False)),
) -> Any:
    await get_experiment_if_accessible_or_raise(id, user)

    experiment = await Experiment.get(id)
    runs = await ExperimentRun.find(
        ExperimentRun.experiment_id == id,
        skip=pagination.offset,
        limit=pagination.limit,
    ).to_list()

    mine = user is not None and experiment.created_by == user["email"]
    return [run.map_to_response(mine=mine) for run in runs]


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
    experiment = await Experiment.get(experiment_run.experiment_id)

    mine = user is not None and experiment.created_by == user["email"]
    return experiment_run.map_to_response(mine=mine, return_detailed_response=True)


@router.get("/experiment-runs/{id}/stop", response_model=None)
async def stop_experiment_run(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=True)),
    workflow_engine: WorkflowEngineBase = Depends(ReanaService.get_service),
) -> Any:
    # TODO this case needs to be properly addressed
    # TODO if this endpoint is executed even before the workflow has even started
    # (the code execution is in _general_workflow_preparation function for example),
    # it will not effectively stop the experiment run execution pipeline and
    # the workflow will be created later on

    experiment_run = await get_experiment_run_if_accessible_or_raise(
        id, user, write_access=True
    )

    experiment = await Experiment.get(experiment_run.experiment_id)
    if experiment.allows_experiment_execution is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot stop this experiment run.",
        )

    await workflow_engine.stop_workflow(experiment_run)
    experiment_run.state = RunState.CRASHED
    await experiment_run.replace()


@router.delete("/experiment-runs/{id}", response_model=None)
async def delete_experiment_run(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=True)),
    workflow_engine: WorkflowEngineBase = Depends(ReanaService.get_service),
) -> Any:
    # TODO this case needs to be properly addressed
    # TODO if this endpoint is executed even before the workflow has even started
    # (the code execution is in _general_workflow_preparation function for example),
    # it will not delete the workflow, however the relevant files as well as the
    # object from the database will be deleted which will cause problems down the line
    # of the experiment run execution pipeline

    experiment_run = await get_experiment_run_if_accessible_or_raise(
        id, user, write_access=True
    )

    experiment = await Experiment.get(experiment_run.experiment_id)
    if experiment.allows_experiment_execution is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot delete this experiment run.",
        )

    await delete_run(experiment_run, workflow_engine)


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
    run_id: PydanticObjectId, user: dict | None, write_access: bool = False
) -> ExperimentRun:
    access_denied_error = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="You cannot access this experiment template",
    )
    experiment_run = await ExperimentRun.get(run_id)

    if experiment_run is None:
        raise access_denied_error
    else:
        # Check the user's accessibility to the experiment, run originated from
        await get_experiment_if_accessible_or_raise(
            experiment_run.experiment_id, user, write_access=write_access
        )
        return experiment_run
