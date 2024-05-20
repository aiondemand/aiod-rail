import logging
from datetime import datetime
from enum import Enum
from pathlib import Path

from pydantic import BaseModel

from app.config import settings


class Pagination(BaseModel):
    offset: int = 0
    limit: int = settings.DEFAULT_RESPONSE_LIMIT


class QueryOperator(str, Enum):
    OR = "OR"
    AND = "AND"


class WorkflowState(BaseModel):
    success: bool
    error_message: str = ""
    manually_stopped: bool = False
    manually_deleted: bool = False


class FileDetail(BaseModel):
    filepath: str
    size: int
    last_modified: datetime


def create_env_file(env_vars: dict[str, str], path: Path) -> None:
    lines = [f"{k}={v}" for k, v in env_vars.items()]
    path.write_text("\n".join(lines))


# TODO
# this function is not being used yet. Having multiple loggers
# with this same setup makes their formatting ugly...
def setup_logger(logger_name: str) -> logging.Logger:
    uvicorn_formatter = logging.getLogger("uvicorn").handlers[0].formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(uvicorn_formatter)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    return logger
