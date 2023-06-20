from typing import Any

from fastapi import APIRouter, Depends
from pydantic import Json

from app.authentication import get_current_user
from app.config import settings
from app.helpers import aiod_client_wrapper
from app.schemas.dataset import Dataset
from app.schemas.publication import Publication

router = APIRouter()


@router.get("/datasets", response_model=list[Dataset])
async def get_datasets(
    offset: int = 0, limit: int = settings.DEFAULT_RESPONSE_LIMIT
) -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        f"{settings.AIOD_API.BASE_URL}/datasets/{settings.AIOD_API.DATASETS_VERSION}",
        params={"offset": offset, "limit": limit},
    )
    return res.json()


@router.get("/counts/datasets", response_model=int)
async def get_datasets_count() -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        f"{settings.AIOD_API.BASE_URL}/counts/datasets/{settings.AIOD_API.DATASETS_VERSION}",
    )
    return res.json()


@router.get("/datasets/{id}", response_model=Dataset)
async def get_dataset(id: int) -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        f"{settings.AIOD_API.BASE_URL}/datasets/{settings.AIOD_API.DATASETS_VERSION}/{id}",
    )
    return res.json()


@router.get("/publications", response_model=list[Publication])
async def get_publications(
    offset: int = 0, limit: int = settings.DEFAULT_RESPONSE_LIMIT
) -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        f"{settings.AIOD_API.BASE_URL}/publications/{settings.AIOD_API.PUBLICATIONS_VERSION}",
        params={"offset": offset, "limit": limit},
    )
    return res.json()


@router.get("/publications/{id}", response_model=Publication)
async def get_publication(id: int) -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        f"{settings.AIOD_API.BASE_URL}/publications/{settings.AIOD_API.PUBLICATIONS_VERSION}/{id}",
    )
    return res.json()


@router.get("/counts/publications", response_model=int)
async def get_publications_count() -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        f"{settings.AIOD_API.BASE_URL}/counts/publications/{settings.AIOD_API.DATASETS_VERSION}",
    )
    return res.json()


@router.get("/authentication_test")
def test_authorization(user: Json = Depends(get_current_user)) -> dict:
    """
    Returns the user, if authenticated correctly.
    """
    return {"msg": "success", "user": user}
