from datetime import datetime

from beanie import Document, PydanticObjectId

from app.models.experiment_template import ExperimentTemplate
from app.schemas.states import TemplateState


class Experiment(Document):
    name: str
    description: str
    publication_ids: list[str]
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    created_by: str

    experiment_template_id: PydanticObjectId
    dataset_ids: list[int]
    model_ids: list[int]
    env_vars: dict[str, str]
    metrics: list[str]

    class Settings:
        name = "experiments"

    async def is_valid(self) -> bool:
        """Validate that experiment matches its experiment template definition"""
        experiment_template = await ExperimentTemplate.get(self.experiment_template_id)

        return (
            await experiment_template.validate_models(self.model_ids)
            and await experiment_template.validate_datasets(self.dataset_ids)
            and experiment_template.validate_env_vars(self.env_vars)
        )

    async def uses_finished_template(self) -> bool:
        """Check whether docker image of ExperimentTemplate has been uploaded"""
        experiment_template = await ExperimentTemplate.get(self.experiment_template_id)
        return experiment_template.state == TemplateState.FINISHED
