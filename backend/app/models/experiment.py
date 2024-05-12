from __future__ import annotations

from datetime import datetime, timezone
from functools import partial

from beanie import Document, PydanticObjectId
from deepdiff import DeepDiff
from pydantic import Field

from app.models.experiment_template import ExperimentTemplate
from app.schemas.env_vars import EnvironmentVar
from app.schemas.experiment import ExperimentCreate, ExperimentResponse
from app.schemas.states import TemplateState


class Experiment(Document):
    name: str
    description: str
    publication_ids: list[str]
    updated_at: datetime = Field(default_factory=partial(datetime.now, tz=timezone.utc))
    created_at: datetime = Field(default_factory=partial(datetime.now, tz=timezone.utc))
    created_by: str
    is_public: bool = False

    experiment_template_id: PydanticObjectId
    dataset_ids: list[int]
    model_ids: list[int]
    env_vars: list[EnvironmentVar]
    metrics: list[str]

    @property
    def assets_attribute_names(self) -> list[str]:
        return [
            "experiment_template_id",
            "publication_ids",
            "dataset_ids",
            "model_ids",
            "env_vars",
            "metrics",
        ]

    class Settings:
        name = "experiments"

    def map_to_response(self) -> ExperimentResponse:
        return ExperimentResponse(**self.dict())

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

    def has_same_assets(self, experiment_req: ExperimentCreate) -> bool:
        return sum(
            [
                bool(
                    DeepDiff(
                        getattr(self, attr_name),
                        getattr(experiment_req, attr_name),
                        ignore_order=True,
                    )
                )
                is False
                for attr_name in self.assets_attribute_names
            ]
        ) == len(self.assets_attribute_names)

    def update_non_assets(self, new_experiment: Experiment) -> None:
        self.name = new_experiment.name
        self.description = new_experiment.description
        self.is_public = new_experiment.is_public  # TODO mozeme toto nastavovat?

    @classmethod
    def update_experiment(
        cls,
        old_experiment: Experiment,
        experiment_req: ExperimentCreate,
        exist_runs: bool,
    ) -> Experiment | None:
        same_assets = old_experiment.has_same_assets(experiment_req)
        new_experiment = Experiment(
            **experiment_req.dict(), created_by=old_experiment.created_by
        )

        if same_assets:
            old_experiment.update_non_assets(new_experiment)
            old_experiment.updated_at = new_experiment.updated_at
            return old_experiment

        if exist_runs is False:
            new_experiment.created_at = old_experiment.created_at
            new_experiment.id = old_experiment.id
            return new_experiment

        return None
