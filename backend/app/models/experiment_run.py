import asyncio
import json
import shutil
from datetime import datetime, timezone
from functools import partial
from pathlib import Path

from beanie import Document, Indexed, PydanticObjectId, operators
from beanie.odm.operators.find import BaseFindOperator
from pydantic import Field

from app.auth import has_admin_role
from app.config import (
    EXPERIMENT_RUN_DIR_PREFIX,
    LOGS_FILENAME,
    METRICS_FILENAME,
    settings,
)
from app.schemas.experiment_run import ExperimentRunDetails, ExperimentRunResponse
from app.schemas.states import RunState


class ExperimentRun(Document):
    experiment_id: Indexed(PydanticObjectId)  # type: ignore
    created_by: str
    created_at: datetime = Field(default_factory=partial(datetime.now, tz=timezone.utc))
    updated_at: datetime = Field(default_factory=partial(datetime.now, tz=timezone.utc))
    retry_count: int = 0
    state: RunState = RunState.CREATED
    is_public: bool
    is_archived: bool = False

    @property
    def logs(self) -> str:
        log_path = self.run_path / LOGS_FILENAME
        return log_path.read_text() if log_path.is_file() else ""

    @property
    def metrics(self) -> dict[str, float]:
        m_path = self.run_output_path / METRICS_FILENAME
        if m_path.exists() is False:
            return {}

        with open(m_path) as f:
            metrics = json.load(f)
        return metrics

    @property
    def workflow_name(self) -> str:
        return f"{EXPERIMENT_RUN_DIR_PREFIX}{str(self.id)}"

    @property
    def run_path(self) -> Path:
        return settings.get_experiment_run_path(self.id)

    @property
    def run_output_path(self) -> Path:
        return settings.get_experiment_run_output_path(self.id)

    class Settings:
        name = "experimentRuns"

    async def update_state_in_db(self, state: RunState) -> None:
        self.state = state
        self.updated_at = datetime.now(tz=timezone.utc)

        await self.set(
            {ExperimentRun.state: self.state, ExperimentRun.updated_at: self.updated_at}
        )

    def map_to_response(
        self, user: dict | None = None, return_detailed_response: bool = False
    ) -> ExperimentRunResponse | ExperimentRunDetails:
        mine = user is not None and self.created_by == user["email"]
        response = ExperimentRunResponse(**self.dict(), metrics=self.metrics, mine=mine)

        if return_detailed_response is False:
            return response
        return ExperimentRunDetails(**response.dict(), logs=self.logs)

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

    def retry_failed_run(self):
        return ExperimentRun(
            experiment_id=self.experiment_id,
            created_by=self.created_by,
            is_public=self.is_public,
            is_archived=self.is_archived,
            retry_count=self.retry_count + 1,
        )

    async def delete_files(self) -> None:
        await asyncio.to_thread(shutil.rmtree, self.run_path)
