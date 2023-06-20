from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel


class ExperimentBase(BaseModel):
    name: str
    description: str
    publication_ids: list[str] = []

    experiment_type_id: PydanticObjectId
    dataset_id: str
    model_id: str
    metrics: list[str]

    save_logs: bool = True
    save_files: bool = True


class ExperimentCreate(ExperimentBase):
    pass


class ExperimentResponse(ExperimentBase):
    id: PydanticObjectId
    created_at: datetime
    updated_at: datetime


class ExperimentType(BaseModel):
    id: PydanticObjectId
    name: str
    description: str
    available_metrics: list[str]
    available_envs: list[str]
