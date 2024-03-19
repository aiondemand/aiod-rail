from io import BytesIO
from typing import Any

from beanie import PydanticObjectId, operators
from beanie.odm.queries.find import FindMany
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse, StreamingResponse
from pydantic import Json

from app.authentication import get_current_user, get_current_user_optional
from app.helpers import FileDetail, Pagination, QueryOperator
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
    user: Json = Depends(get_current_user_optional),
    pagination: Pagination = Depends(),
    include_mine: bool = False,
    query_operator: QueryOperator = QueryOperator.AND,
) -> Any:
    result_set = find_specific_experiments(
        include_mine=include_mine,
        query_operator=query_operator,
        user=user,
        pagination=pagination,
    )
    experiments = await result_set.to_list()

    return [experiment.dict() for experiment in experiments]


@router.get(
    "/count/experiments",
    response_model=int,
)
async def get_experiments_count(
    user: Json = Depends(get_current_user_optional),
    include_mine: bool = False,
    query_operator: QueryOperator = QueryOperator.AND,
) -> Any:
    result_set = find_specific_experiments(
        include_mine=include_mine, query_operator=query_operator, user=user
    )
    return await result_set.count()


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
    user: Json = Depends(get_current_user),
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
    if not await workflow_engine.is_connected():
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
    id: PydanticObjectId, pagination: Pagination = Depends()
) -> Any:
    runs = await ExperimentRun.find(
        ExperimentRun.experiment_id == id,
        skip=pagination.offset,
        limit=pagination.limit,
    ).to_list()

    return [run.map_to_response() for run in runs]


@router.get("/count/experiments/{id}/runs", response_model=int)
async def get_experiment_runs_count(id: PydanticObjectId) -> Any:
    runs = await ExperimentRun.find(ExperimentRun.experiment_id == id)
    return len(runs)


@router.get("/experiment-runs", response_model=list[ExperimentRunResponse])
async def get_all_experiment_runs(pagination: Pagination = Depends()) -> Any:
    runs = await ExperimentRun.find_all(
        skip=pagination.offset, limit=pagination.limit
    ).to_list()
    return [run.map_to_response() for run in runs]


@router.get("/experiment-runs/{id}", response_model=ExperimentRunDetails | None)
async def get_experiment_run(id: PydanticObjectId) -> Any:
    experiment_run = await ExperimentRun.get(id)
    return experiment_run.map_to_detailed_response()


@router.get("/experiment-runs/{id}/logs", response_class=PlainTextResponse)
async def get_experiment_run_logs(id: PydanticObjectId) -> str:
    experiment_run = await ExperimentRun.get(id)
    return experiment_run.logs


@router.get("/experiment-runs/{id}/files/download", response_class=StreamingResponse)
async def download_file(
    id: PydanticObjectId,
    filepath: str,
    workflow_engine: WorkflowEngineBase = Depends(ReanaService.get_service),
) -> bytes:
    experiment_run = await ExperimentRun.get(id)
    data, save_name = await workflow_engine.download_file(experiment_run, filepath)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Requested file doesn't exist.",
        )

    buffer = BytesIO(data)

    def chunk_generator():
        CHUNK_SIZE = 1024**2  # 1MB chunks
        while chunk := buffer.read(CHUNK_SIZE):
            yield chunk

    headers = {"Content-Disposition": f'attachment; filename="{save_name}"'}
    return StreamingResponse(
        chunk_generator(), headers=headers, media_type="application/octet-stream"
    )


@router.get("/experiment-runs/{id}/files/list", response_model=list[FileDetail])
async def list_files(
    id: PydanticObjectId,
    path: str = "",
    workflow_engine: WorkflowEngineBase = Depends(ReanaService.get_service),
) -> list[str]:
    experiment_run = await ExperimentRun.get(id)
    return await workflow_engine.list_files(experiment_run, path)


def find_specific_experiments(
    include_mine: bool,
    query_operator: QueryOperator,
    user: Json,
    pagination: Pagination = None,
) -> FindMany[Experiment]:
    search_conditions = []
    page_kwargs = (
        {"skip": pagination.offset, "limit": pagination.limit}
        if pagination is not None
        else {}
    )

    if len(user) == 0 and include_mine:
        # You need to be authorized to see only your experiments
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This endpoint requires authorization. You need to be logged in.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if len(user) == 0:
        # for now this if block is redundant, but once there is more
        # queries, it might be relevant
        include_mine = False
    if include_mine:
        search_conditions.append(Experiment.created_by == user["email"])

    if len(search_conditions) > 0:
        multi_query = (
            operators.Or(*search_conditions)
            if query_operator == QueryOperator.OR
            else operators.And(*search_conditions)
        )
        return Experiment.find(multi_query, **page_kwargs)

    return Experiment.find_all(**page_kwargs)
