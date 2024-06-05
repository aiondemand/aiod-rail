from datetime import datetime
from pathlib import Path
from typing import Any

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse, StreamingResponse

from app.auth import get_current_user
from app.config import TEMP_DIRNAME
from app.helpers import FileDetail
from app.models.experiment_run import ExperimentRun
from app.schemas.experiment_run import ExperimentRunDetails
from app.schemas.states import RunState
from app.services.workflow_engines.base import WorkflowEngineBase
from app.services.workflow_engines.reana import ReanaService

router = APIRouter()


@router.get("/experiment-runs/{id}", response_model=ExperimentRunDetails | None)
async def get_experiment_run(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=False, from_api_key=True)),
) -> Any:
    experiment_run = await get_experiment_run_if_accessible_or_raise(id, user)
    return experiment_run.map_to_response(user, return_detailed_response=True)


# TODO this function is commented out to prevent anyone from using for now
# @router.get("/experiment-runs/{id}/stop", response_model=None)
# async def stop_experiment_run(
#     id: PydanticObjectId,
#     user: dict = Depends(get_current_user(required=True, from_api_key=True)),
#     workflow_engine: WorkflowEngineBase = Depends(ReanaService.get_service),
# ) -> Any:
#     # TODO this case needs to be properly addressed
#     # TODO if this endpoint is executed even before the workflow has even started
#     # (the code execution is in _general_workflow_preparation function for example),
#     # it will not effectively stop the experiment run execution pipeline and
#     # the workflow will be created later on

#     experiment_run = await get_experiment_run_if_accessible_or_raise(
#         id, user, write_access=True
#     )
#     if experiment_run.is_archived:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="You cannot stop this experiment run.",
#         )

#     await workflow_engine.stop_workflow(experiment_run)
#     await experiment_run.update_state_in_db(RunState.CRASHED)


@router.delete("/experiment-runs/{id}", response_model=None)
async def delete_experiment_run(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=True, from_api_key=True)),
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

    # TODO for now we can only delete experiment runs that have already been finished
    if (
        experiment_run.state not in [RunState.FINISHED, RunState.CRASHED]
        or experiment_run.is_archived
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot delete this experiment run.",
        )

    await delete_run(experiment_run, workflow_engine)


@router.get("/experiment-runs/{id}/logs", response_class=PlainTextResponse)
async def get_experiment_run_logs(
    id: PydanticObjectId,
    user: dict = Depends(get_current_user(required=False, from_api_key=True)),
) -> str:
    experiment_run = await get_experiment_run_if_accessible_or_raise(id, user)
    return experiment_run.logs


@router.get("/experiment-runs/{id}/files/download", response_class=StreamingResponse)
async def download_file_from_experiment_run(
    id: PydanticObjectId,
    filepath: str,
    workflow_engine: WorkflowEngineBase = Depends(ReanaService.get_service),
    user: dict = Depends(get_current_user(required=False, from_api_key=True)),
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
    user: dict = Depends(get_current_user(required=False, from_api_key=True)),
) -> list[FileDetail]:
    experiment_run = await get_experiment_run_if_accessible_or_raise(id, user)
    return await workflow_engine.list_files(experiment_run)


async def get_experiment_run_if_accessible_or_raise(
    run_id: PydanticObjectId, user: dict | None, write_access: bool = False
) -> ExperimentRun:
    access_denied_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You cannot access this experiment run",
    )
    experiment_run = await ExperimentRun.get(run_id)

    if experiment_run is None:
        raise access_denied_error
    else:
        if write_access and experiment_run.is_editable_by_user(user):
            return experiment_run
        elif not write_access and experiment_run.is_readable_by_user(user):
            return experiment_run
        else:
            raise access_denied_error


async def set_public_run(run: ExperimentRun, value: bool, updated_at: datetime) -> None:
    await run.set(
        {ExperimentRun.is_public: value, ExperimentRun.updated_at: updated_at}
    )


async def set_archived_run(
    run: ExperimentRun, value: bool, updated_at: datetime
) -> None:
    await run.set(
        {ExperimentRun.is_archived: value, ExperimentRun.updated_at: updated_at}
    )


async def delete_run(run: ExperimentRun, workflow_engine: WorkflowEngineBase) -> None:
    await workflow_engine.delete_workflow(run)
    await ExperimentRun.find(ExperimentRun.id == run.id).delete()
    await run.delete_files()
