import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.authentication import get_current_user
from app.models.rail_user import RailUser
from app.schemas.rail_user import RailUserResponse

logger = logging.getLogger("uvicorn")

router = APIRouter()


@router.get("/users/profile", response_model=RailUserResponse)
async def get_user_profile(
    user: dict = Depends(get_current_user(required=True)),
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


@router.get("/users/api_key", response_model=str)
async def get_user_api_key(
    user: dict = Depends(get_current_user(required=False)),
) -> Any:
    user_obj = await RailUser.find_one(RailUser.email == user["email"])

    if not user_obj or user_obj.api_key == "":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found",
        )
    return user_obj["api_key"]


@router.post("/users/api_key", response_model=str)
async def create_or_change_user_api_key(
    user: dict = Depends(get_current_user(required=True)),
) -> Any:
    user_obj = await RailUser.find_one(RailUser.email == user["email"])

    if not user_obj:
        try:
            user_obj = await RailUser(
                email=user["email"], api_key=RailUser.generate_api_key()
            ).create()
        except Exception:
            logger.error("Error while creating user profile and API key")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error while creating user profile and API key",
            )
    elif not user_obj.api_key:
        try:
            user_obj.api_key = RailUser.generate_api_key()
            await RailUser.replace(user_obj)
        except Exception:
            logger.error("Error while creating API key")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error while creating API key",
            )

    return user_obj.api_key
