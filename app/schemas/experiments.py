from beanie import PydanticObjectId
from pydantic import BaseModel


class ExperimentBase(BaseModel):
    dataset_ids: list[str]
    publication_ids: list[str]


class ExperimentCreate(ExperimentBase):
    pass


class ExperimentResponse(ExperimentBase):
    id: PydanticObjectId
