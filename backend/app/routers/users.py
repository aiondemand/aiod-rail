from fastapi import APIRouter, Depends, HTTPException, logger, status

from app.authentication import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse


router = APIRouter()

@router.get("/users/profile")
async def get_user_profile(
    user: dict = Depends(get_current_user(required=True))
) -> UserResponse:    
    try:
        user_obj = await User.find_one({"email": user["email"]})
        
        if not user_obj:
            user_obj = await User(email=user["email"]).create()
    except Exception:
        logger.error("Error while fetching or creating user profile")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while fetching or creating user profile",
        )

    return user_obj.map_to_response()

@router.get("/users/api_key")
async def get_user_api_key(
    user: dict = Depends(get_current_user(required=False))
) -> str:
    user = await User.find_one({"email": user["email"]})
    
    if not user or "api_key" not in user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found",
        )
    return user["api_key"]

@router.post("/users/api_key")
async def create_or_change_user_api_key(
    user: dict = Depends(get_current_user(required=True))
) -> str:
    user_obj = await User.find_one({"email": user["email"]})
    
    if not user_obj:
        try:
            user_obj = await User(
                email=user["email"], 
                api_key=User.generate_api_key()
            ).create()
        except Exception:
            logger.error("Error while creating user profile and API key")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error while creating user profile and API key",
            )
    elif "api_key" not in user_obj or not user_obj.api_key:
        try:
            user_obj.api_key = User.generate_api_key()
            await User.replace(user_obj)
        except Exception:
            logger.error("Error while creating API key")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error while creating API key",
            )

    return user_obj.api_key
