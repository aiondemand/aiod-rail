from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel

from app.schemas.env_vars import EnvironmentVar


class ExperimentBase(BaseModel):
    name: str
    description: str
    is_public: bool

    experiment_template_id: PydanticObjectId
    dataset_ids: list[str]
    model_ids: list[str]
    publication_ids: list[str] = []
    env_vars: list[EnvironmentVar]


class ExperimentCreate(ExperimentBase):
    pass


class ExperimentResponse(ExperimentBase):
    id: PydanticObjectId
    created_at: datetime
    updated_at: datetime
    is_archived: bool
    is_mine: bool
