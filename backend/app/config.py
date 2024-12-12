from functools import lru_cache
from pathlib import Path

from pydantic import AnyHttpUrl, BaseModel, BaseSettings, DirectoryPath

USERDATA_DIRNAME = "experiments-userdata"
EXPERIMENT_TEMPLATES_DIRNAME = "experiment-templates"
EXPERIMENT_RUN_DIR_PREFIX = "run-"
EXPERIMENT_TEMPLATE_DIR_PREFIX = "template-"
METRICS_FILENAME = "metrics.json"
LOGS_FILENAME = "logs.txt"
LITTLE_NAP = 5
CHECK_REANA_CONNECTION_INTERVAL = 60
RUN_TEMP_OUTPUT_FOLDER = "output-temp"
RUN_OUTPUT_FOLDER = "output"
REPOSITORY_NAME = "rail-exp-templates"
TEMP_DIRNAME = "temp"


class AIoDApiConfig(BaseModel):
    BASE_URL: AnyHttpUrl
    DATASETS_VERSION: str = "v1"
    ML_MODELS_VERSION: str = "v1"
    PUBLICATIONS_VERSION: str = "v1"
    PLATFORMS_VERSION: str = "v1"


class AIoDLibraryApiConfig(BaseModel):
    BASE_URL: AnyHttpUrl


class AIoDEnhancedSearchApiConfig(BaseModel):
    BASE_URL: AnyHttpUrl


class AIODKeycloakConfig(BaseModel):
    REALM: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    SERVER_URL: AnyHttpUrl
    OIDC_URL: AnyHttpUrl


class Settings(BaseSettings):
    MONGODB_URI: str
    MONGODB_DBNAME: str

    AIOD_API: AIoDApiConfig
    AIOD_LIBRARY_API: AIoDLibraryApiConfig
    AIOD_ENHANCED_SEARCH_API: AIoDEnhancedSearchApiConfig
    AIOD_KEYCLOAK: AIODKeycloakConfig
    DEFAULT_RESPONSE_LIMIT: int = 100

    # TODO: clean
    DOCKER_BASE_URL: str
    DOCKER_REGISTRY_URL: str
    DOCKER_REGISTRY_USERNAME: str
    DOCKER_REGISTRY_PASSWORD: str

    REANA_SERVER_URL: str
    REANA_ACCESS_TOKEN: str

    EEE_DATA_PATH: DirectoryPath
    MAX_PARALLEL_IMAGE_BUILDS: int = 2
    MAX_PARALLEL_CONTAINERS: int = 2
    MAX_IMAGE_BUILDS_ATTEMPTS: int = 1
    MAX_EXPERIMENT_RUN_ATTEMPTS: int = 1

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
        case_sensitive = True

    @property
    def userdata_path(self) -> Path:
        return self.EEE_DATA_PATH / USERDATA_DIRNAME

    @property
    def experiment_templates_path(self) -> Path:
        return self.EEE_DATA_PATH / EXPERIMENT_TEMPLATES_DIRNAME

    def get_experiment_run_path(self, run_id: str) -> Path:
        return self.userdata_path / f"{EXPERIMENT_RUN_DIR_PREFIX}{run_id}"

    def get_experiment_template_path(self, template_id: str) -> Path:
        return (
            self.experiment_templates_path
            / f"{EXPERIMENT_TEMPLATE_DIR_PREFIX}{template_id}"
        )

    def get_experiment_run_output_path(self, run_id: str) -> Path:
        return self.get_experiment_run_path(run_id) / RUN_OUTPUT_FOLDER


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
