from datetime import datetime, timezone
from typing import Any

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.auth import is_admin
from app.models.experiment_template import ExperimentTemplate
from app.services.experiment_scheduler import ExperimentScheduler

router = APIRouter(dependencies=[Depends(is_admin)])


@router.patch(
    "/experiment-templates/{id}/approve",
    response_model=None,
)
async def approve_experiment_template(
    id: PydanticObjectId,
    approve: bool = False,
    exp_scheduler: ExperimentScheduler = Depends(ExperimentScheduler.get_service),
) -> Any:
    experiment_template = await ExperimentTemplate.get(id)
    if experiment_template is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Such experiment template doesn't exist",
        )

    experiment_template.approved = approve
    experiment_template.updated_at = datetime.now(tz=timezone.utc)

    await ExperimentTemplate.replace(experiment_template)

    if approve:
        await exp_scheduler.add_image_to_build(experiment_template.id)
