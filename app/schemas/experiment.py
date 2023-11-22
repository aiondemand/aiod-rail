from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel


class ExperimentBase(BaseModel):
    name: str
    description: str
    publication_ids: list[str] = []

    experiment_template_id: PydanticObjectId
    dataset_ids: list[str]
    model_ids: list[str]
    env_vars: dict[str, str]
    metrics: list[str]


class ExperimentCreate(ExperimentBase):
    pass


class ExperimentResponse(ExperimentBase):
    id: PydanticObjectId
    created_at: datetime
    updated_at: datetime
