from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel

from app.schemas.env_vars import EnvironmentVar


class ExperimentBase(BaseModel):
    name: str
    description: str
    experiment_template_id: PydanticObjectId

    publication_ids: list[str] = []
    dataset_ids: list[str]
    model_ids: list[str]

    env_vars: list[EnvironmentVar]
    metrics: list[str]
    is_public: bool


class ExperimentCreate(ExperimentBase):
    pass


class ExperimentResponse(ExperimentBase):
    id: PydanticObjectId
    created_at: datetime
    updated_at: datetime
    is_usable: bool
