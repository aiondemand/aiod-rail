import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import get_current_user_or_raise
from app.models.rail_user import RailUser
from app.schemas.rail_user import RailUserResponse

logger = logging.getLogger("uvicorn")

router = APIRouter()


@router.get("/users/profile", response_model=RailUserResponse)
async def get_user_profile(
    user: dict = Depends(get_current_user_or_raise),
) -> Any:
    try:
        user_obj = await RailUser.find_one(RailUser.email == user["email"])

        if not user_obj:
            user_obj = await RailUser(email=user["email"]).create()
    except Exception:
        logger.error("Error while fetching or creating user profile")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while fetching or creating user profile",
        )

    return user_obj.map_to_response()
