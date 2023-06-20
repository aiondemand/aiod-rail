from functools import lru_cache

from pydantic import AnyHttpUrl, BaseModel, BaseSettings


class AIODApiSettings(BaseModel):
    BASE_URL: AnyHttpUrl
    DATASETS_VERSION: str = "v0"
    PUBLICATIONS_VERSION: str = "v0"


class AIODKeycloakSettings(BaseModel):
    REALM: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    SERVER_URL: str

class Settings(BaseSettings):
    MONGODB_URI: str
    MONGODB_DBNAME: str

    AIOD_API: AIODApiSettings
    AIOD_KEYCLOAK: AIODKeycloakSettings
    DEFAULT_RESPONSE_LIMIT: int = 100

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
