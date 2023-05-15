from functools import lru_cache

from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    METADATA_API_BASE_URL: AnyHttpUrl

    MONGODB_URI: str
    MONGODB_DBNAME: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
