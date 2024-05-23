from __future__ import annotations

from datetime import datetime, timezone
from functools import partial

import pymongo
from beanie import Document, Indexed, PydanticObjectId
from deepdiff import DeepDiff
from pydantic import Field

from app.models.experiment_template import ExperimentTemplate
from app.schemas.env_vars import EnvironmentVar
from app.schemas.experiment import ExperimentCreate, ExperimentResponse


class Experiment(Document):
    name: Indexed(str, index_type=pymongo.TEXT)  # type: ignore
    description: str
    updated_at: datetime = Field(default_factory=partial(datetime.now, tz=timezone.utc))
    created_at: datetime = Field(default_factory=partial(datetime.now, tz=timezone.utc))
    created_by: str
    public: bool = False
    archived: bool = False

    experiment_template_id: PydanticObjectId

    publication_ids: list[int]
    dataset_ids: list[int]
    model_ids: list[int]

    env_vars: list[EnvironmentVar]

    @property
    def assets_attribute_names(self) -> list[str]:
        return [
            "experiment_template_id",
            "publication_ids",
            "dataset_ids",
            "model_ids",
            "env_vars",
        ]

    @property
    def allows_experiment_execution(self) -> bool:
        return self.archived is False

    class Settings:
        name = "experiments"

    def map_to_response(self, user: dict | None = None) -> ExperimentResponse:
        mine = user is not None and self.created_by == user["email"]
        return ExperimentResponse(**self.dict(), mine=mine)

    async def is_valid(self, experiment_template: ExperimentTemplate) -> bool:
        """Validate that experiment matches its experiment template definition"""
        return (
            await experiment_template.validate_models(self.model_ids)
            and await experiment_template.validate_datasets(self.dataset_ids)
            and experiment_template.validate_env_vars(self.env_vars)
        )

    def has_same_assets(self, experiment: Experiment) -> bool:
        return sum(
            [
                bool(
                    DeepDiff(
                        getattr(self, attr_name),
                        getattr(experiment, attr_name),
                        ignore_order=True,
                    )
                )
                is False
                for attr_name in self.assets_attribute_names
            ]
        ) == len(self.assets_attribute_names)

    @classmethod
    async def update_experiment(
        cls,
        original_experiment: Experiment,
        experiment_req: ExperimentCreate,
        new_template: ExperimentTemplate,
        editable_assets: bool,
    ) -> Experiment | None:
        new_experiment = Experiment(
            **experiment_req.dict(), created_by=original_experiment.created_by
        )
        same_template = (
            original_experiment.experiment_template_id
            == new_experiment.experiment_template_id
        )
        same_assets = original_experiment.has_same_assets(new_experiment)

        if not await new_experiment.is_valid(new_template) or (
            # we check whether we update a new experiment template to
            # an archived one
            same_template is False
            and new_template.allows_experiment_creation is False
        ):
            return None

        experiment_to_return = None
        if same_assets:
            # Update name, descr & visibility
            original_experiment.name = new_experiment.name
            original_experiment.description = new_experiment.description
            original_experiment.public = new_experiment.public

            original_experiment.updated_at = new_experiment.updated_at
            experiment_to_return = original_experiment

        elif editable_assets:
            # No runs exist yet, so we can change everything in experiment
            new_experiment.created_at = original_experiment.created_at
            new_experiment.id = original_experiment.id
            experiment_to_return = new_experiment

        return experiment_to_return
