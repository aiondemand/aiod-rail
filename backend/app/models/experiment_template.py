from datetime import datetime

import yaml
from beanie import Document

from app.config import (
    EXPERIMENT_TEMPLATE_DIR_PREFIX,
    REPOSITORY_NAME,
    RUN_TEMP_OUTPUT_FOLDER,
    settings,
)
from app.routers.aiod import get_dataset_name, get_model_name
from app.schemas.env_vars import EnvironmentVar, EnvironmentVarDef
from app.schemas.experiment_template import (
    AssetSchema,
    ExperimentTemplateResponse,
    TaskType,
)
from app.schemas.states import TemplateState


class ExperimentTemplate(Document):
    name: str
    description: str
    task: TaskType
    datasets_schema: AssetSchema
    models_schema: AssetSchema
    envs_required: list[EnvironmentVarDef]
    envs_optional: list[EnvironmentVarDef]
    available_metrics: list[str]
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    state: TemplateState = TemplateState.CREATED
    approved: bool = False
    created_by: str

    class Settings:
        name = "experimentTemplates"

    def initialize_files(self, base_image, pip_requirements, script):
        base_path = settings.get_experiment_template_path(template_id=self.id)
        base_path.mkdir(exist_ok=True, parents=True)

        with open("app/data/template-Dockerfile") as f:
            dockerfile_template_lines = f.readlines()
            dockerfile_template_lines[0] = f"FROM {base_image}\n"
            dockerfile = "".join(dockerfile_template_lines)

        base_path.joinpath("Dockerfile").write_text(dockerfile)
        base_path.joinpath("requirements.txt").write_text(pip_requirements)
        base_path.joinpath("script.py").write_text(script)

        reana_cfg = yaml.safe_load(open("app/data/template-reana.yaml"))
        reana_cfg["workflow"]["specification"]["steps"][0][
            "environment"
        ] = self.get_image_name()
        reana_cfg["outputs"]["directories"][0] = RUN_TEMP_OUTPUT_FOLDER

        with base_path.joinpath("reana.yaml").open("w") as fp:
            yaml.safe_dump(reana_cfg, fp)

    def map_to_response(self) -> ExperimentTemplateResponse:
        experiment_template_path = settings.get_experiment_template_path(
            template_id=self.id
        )

        return ExperimentTemplateResponse(
            **self.dict(),
            dockerfile=experiment_template_path.joinpath("Dockerfile").read_text(),
            pip_requirements=experiment_template_path.joinpath(
                "requirements.txt"
            ).read_text(),
            script=experiment_template_path.joinpath("script.py").read_text(),
        )

    def update_state(self, state: TemplateState) -> None:
        self.state = state
        self.updated_at = datetime.utcnow()

    async def validate_models(self, model_ids: list[int]) -> bool:
        model_names = [await get_model_name(x) for x in model_ids]

        checks = [
            all(model_name is not None for model_name in model_names),
            self.models_schema.cardinality.is_valid(len(model_names)),
        ]

        return all(checks)

    async def validate_datasets(self, dataset_ids: list[int]) -> bool:
        dataset_names = [await get_dataset_name(x) for x in dataset_ids]

        checks = [
            all(dataset_name is not None for dataset_name in dataset_names),
            self.datasets_schema.cardinality.is_valid(len(dataset_names)),
        ]

        return all(checks)

    def validate_env_vars(self, env_vars: list[EnvironmentVar]) -> bool:
        experiment_environment_var_names = set([env.key for env in env_vars])
        required_environment_var_names = set([env.name for env in self.envs_required])

        return required_environment_var_names.issubset(experiment_environment_var_names)

    def get_image_name(self) -> str:
        image_tag = f"{EXPERIMENT_TEMPLATE_DIR_PREFIX}{self.id}"
        return f"{settings.DOCKER_REGISTRY_URL}/{REPOSITORY_NAME}:{image_tag}"
