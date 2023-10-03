from datetime import datetime

from beanie import Document, PydanticObjectId


class Experiment(Document):
    name: str
    description: str
    publication_ids: list[str]
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    created_by: str

    experiment_type_id: PydanticObjectId
    dataset_ids: list[int]
    model_ids: list[int]
    metrics: list[str]

    save_logs: bool
    save_files: bool

    class Settings:
        name = "experiments"
