from fastapi import APIRouter

from app.config import settings
from app.helpers import aiod_client_wrapper

router = APIRouter()


@router.get("/datasets")
async def get_datasets(offset: int = 0, limit: int = settings.DEFAULT_RESPONSE_LIMIT):
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        f"{settings.AIOD_API.BASE_URL}/datasets/{settings.AIOD_API.DATASETS_VERSION}",
        params={"offset": offset, "limit": limit},
    )
    return res.json()


@router.get("/datasets/{id}")
async def get_datasets(id: int):
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        f"{settings.AIOD_API.BASE_URL}/datasets/{settings.AIOD_API.DATASETS_VERSION}/{id}",
    )
    return res.json()


@router.get("/publications")
async def get_publications(
    offset: int = 0, limit: int = settings.DEFAULT_RESPONSE_LIMIT
):
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        f"{settings.AIOD_API.BASE_URL}/publications/{settings.AIOD_API.PUBLICATIONS_VERSION}",
        params={"offset": offset, "limit": limit},
    )
    return res.json()


@router.get("/publications/{id}")
async def get_datasets(id: int):
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        f"{settings.AIOD_API.BASE_URL}/publications/{settings.AIOD_API.PUBLICATIONS_VERSION}/{id}",
    )
    return res.json()
