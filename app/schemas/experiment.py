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
    task: str
    datasets_schema: dict
    models_schema: dict
    envs_required: list[str]
    envs_optional: list[str]
    available_metrics: list[str]
    dockerfile: str
    script: str
    pip_requirements: str


class ExperimentRunBase(BaseModel):
    id: PydanticObjectId
    created_at: datetime
    updated_at: datetime
    status: str


class ExperimentRunExecute(BaseModel):
    id: PydanticObjectId
    experiment_type_id: PydanticObjectId
    dataset_names: list[str]
    model_names: list[str]
    env_vars: dict[str, str]
    metrics: list[str]


class ExperimentRun(ExperimentRunBase):
    pass


class ExperimentRunDetails(ExperimentRunBase):
    metrics: dict
