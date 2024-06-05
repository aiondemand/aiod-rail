from __future__ import annotations

from datetime import datetime, timezone
from functools import partial

import pymongo
from beanie import Document, Indexed, PydanticObjectId, operators
from beanie.odm.operators.find import BaseFindOperator
from deepdiff import DeepDiff
from pydantic import Field

from app.auth import has_admin_role
from app.models.experiment_template import ExperimentTemplate
from app.schemas.env_vars import EnvironmentVar
from app.schemas.experiment import ExperimentCreate, ExperimentResponse


class Experiment(Document):
    name: Indexed(str, index_type=pymongo.TEXT)  # type: ignore
    description: str
    created_by: str
    created_at: datetime = Field(default_factory=partial(datetime.now, tz=timezone.utc))
    updated_at: datetime = Field(default_factory=partial(datetime.now, tz=timezone.utc))
    is_public: bool = False
    is_archived: bool = False

    experiment_template_id: PydanticObjectId
    dataset_ids: list[int]
    model_ids: list[int]
    publication_ids: list[int]
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
    def allows_execution(self) -> bool:
        return self.is_archived is False

    class Settings:
        name = "experiments"

    @classmethod
    async def create_experiment(
        cls,
        experiment_req: ExperimentCreate,
        template: ExperimentTemplate,
        created_by: str,
    ) -> Experiment:
        kwargs = experiment_req.dict()
        kwargs["env_vars"] = [
            EnvironmentVar.create_variable(
                var, template.envs_required + template.envs_optional
            )
            for var in experiment_req.env_vars
        ]

        experiment = Experiment(**kwargs, created_by=created_by)
        if not await experiment.is_valid(template):
            return None

        return experiment

    def map_to_response(self, user: dict | None = None) -> ExperimentResponse:
        is_mine = user is not None and self.created_by == user["email"]
        for var in self.env_vars:
            var.censor(is_mine)

        return ExperimentResponse(**self.dict(), is_mine=is_mine)

    def is_readable_by_user(self, user: dict | None) -> bool:
        if self.is_public:
            return True
        elif user is None:
            return False
        else:
            return self.created_by == user["email"] or has_admin_role(user)

    @classmethod
    def get_query_readable_by_user(cls, user: dict | None) -> BaseFindOperator:
        if user is None:
            return operators.Eq(cls.is_public, True)
        elif has_admin_role(user):
            return operators.Exists(cls.id, True)
        else:
            return operators.Or(
                operators.Eq(cls.is_public, True),
                operators.Eq(cls.created_by, user["email"]),
            )

    def is_editable_by_user(self, user: dict | None) -> bool:
        if user is not None and self.created_by == user["email"]:
            return True
        else:
            return False

    async def is_valid(self, experiment_template: ExperimentTemplate) -> bool:
        """Validate that experiment matches its experiment template definition"""
        return (
            await experiment_template.validate_models(self.model_ids)
            and await experiment_template.validate_datasets(self.dataset_ids)
            and experiment_template.validate_env_vars(self.env_vars)
        )

    def has_same_assets(self, experiment: Experiment) -> bool:
        return all(
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
        )

    @classmethod
    async def update_experiment(
        cls,
        original_experiment: Experiment,
        experiment_req: ExperimentCreate,
        new_template: ExperimentTemplate,
        editable_assets: bool,
    ) -> Experiment | None:
        new_experiment = await Experiment.create_experiment(
            experiment_req, new_template, created_by=original_experiment.created_by
        )
        if new_experiment is None:
            return None

        same_template = (
            original_experiment.experiment_template_id
            == new_experiment.experiment_template_id
        )
        same_assets = original_experiment.has_same_assets(new_experiment)

        if same_template is False and new_template.allows_experiment_creation is False:
            return None

        experiment_to_return = None
        if same_assets:
            # Update name, descr & visibility
            original_experiment.name = new_experiment.name
            original_experiment.description = new_experiment.description
            original_experiment.is_public = new_experiment.is_public

            original_experiment.updated_at = new_experiment.updated_at
            experiment_to_return = original_experiment

        elif editable_assets:
            # No runs exist yet, so we can change everything in experiment
            new_experiment.created_at = original_experiment.created_at
            new_experiment.id = original_experiment.id
            experiment_to_return = new_experiment

        return experiment_to_return
