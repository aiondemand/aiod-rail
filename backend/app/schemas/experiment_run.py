from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel

from app.schemas.states import RunState


class ExperimentRunBase(BaseModel):
    id: PydanticObjectId
    created_at: datetime
    updated_at: datetime
    retry_count: int
    state: RunState
    metrics: dict[str, float]
    mine: bool
    experiment_id: PydanticObjectId


class ExperimentRunResponse(ExperimentRunBase):
    pass


class ExperimentRunDetails(ExperimentRunBase):
    logs: str


class ExperimentRunId(BaseModel):
    """
    A class that is used for projecting the entire ExperimentRun documents
    into only their IDs and that we use when fetching ExperimentRun documents.
    Using the beanie library, we cannot simply choose what fields to return,
    but rather we need to create a projection definition using a separate class.
    """

    id: PydanticObjectId

    class Settings:
        projection = {"id": "$_id"}
