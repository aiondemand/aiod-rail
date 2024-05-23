from datetime import datetime
from enum import Enum

from beanie import PydanticObjectId
from pydantic import BaseModel

from app.schemas.env_vars import EnvironmentVarDef
from app.schemas.states import TemplateState


class TaskType(str, Enum):
    IMAGE_CLASSIFICATION = "IMAGE_CLASSIFICATION"
    OBJECT_DETECTION = "OBJECT_DETECTION"
    TEXT_CLASSIFICATION = "TEXT_CLASSIFICATION"
    TOKEN_CLASSIFICATION = "TOKEN_CLASSIFICATION"
    QUESTION_ANSWERING = "QUESTION_ANSWERING"
    TRANSLATION = "TRANSLATION"
    SUMMARIZATION = "SUMMARIZATION"
    TEXT_GENERATION = "TEXT_GENERATION"
    OTHER = "OTHER"


class AssetCardinality(str, Enum):
    ZERO_OR_MANY = "0-N"
    ONE_OR_MANY = "1-N"
    ONE = "1-1"

    def is_valid(self, value: int) -> bool:
        lower, upper = self.value.split("-")
        return value >= int(lower) and (upper == "N" or value <= int(upper))


class AssetSchema(BaseModel):
    cardinality: AssetCardinality


class ExperimentTemplateBase(BaseModel):
    name: str
    description: str
    task: TaskType
    datasets_schema: AssetSchema
    models_schema: AssetSchema
    envs_required: list[EnvironmentVarDef]
    envs_optional: list[EnvironmentVarDef]
    script: str
    pip_requirements: str
    public: bool


class ExperimentTemplateCreate(ExperimentTemplateBase):
    base_image: str


class ExperimentTemplateResponse(ExperimentTemplateBase):
    id: PydanticObjectId
    created_at: datetime
    updated_at: datetime
    state: TemplateState
    dockerfile: str
    approved: bool
    archived: bool
    mine: bool


class ExperimentTemplateId(BaseModel):
    """
    A class that is used for projecting the entire ExperimentTemplate documents
    into only their IDs and that we use when fetching ExperimentTemplate documents.
    Using the beanie library, we cannot simply choose what fields to return,
    but rather we need to create a projection definition using a separate class.
    """

    id: PydanticObjectId

    class Settings:
        projection = {"id": "$_id"}
