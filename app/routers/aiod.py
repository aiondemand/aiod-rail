from typing import Any

from fastapi import APIRouter, Depends
from pydantic import Json

from app.authentication import get_current_user
from app.config import settings
from app.dummy_code import (
    Model,
    get_dummy_model,
    get_dummy_model_count,
    get_dummy_models,
)
from app.helpers import Pagination, aiod_client_wrapper
from app.schemas.dataset import Dataset
from app.schemas.publication import Publication

router = APIRouter()


@router.get("/datasets", response_model=list[Dataset])
async def get_datasets(pagination: Pagination = Depends()) -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        f"{settings.AIOD_API.BASE_URL}/datasets/{settings.AIOD_API.DATASETS_VERSION}",
        params={"offset": pagination.offset, "limit": pagination.limit},
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
async def get_publications(pagination: Pagination = Depends()) -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        f"{settings.AIOD_API.BASE_URL}/publications/{settings.AIOD_API.PUBLICATIONS_VERSION}",
        params={"offset": pagination.offset, "limit": pagination.limit},
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
        f"{settings.AIOD_API.BASE_URL}/counts/publications/{settings.AIOD_API.PUBLICATIONS_VERSION}",
    )
    return res.json()


@router.get("/models", response_model=list[Model])
async def get_models(pagination: Pagination = Depends()) -> Any:
    # TODO: Replace this dummy response
    return get_dummy_models()


@router.get("/models/{id}", response_model=Model)
async def get_model(id: int) -> Any:
    # TODO: Replace this dummy response
    return get_dummy_model(id=id)


@router.get("/counts/models", response_model=int)
async def get_models_count() -> Any:
    # TODO: Replace this dummy response
    return get_dummy_model_count()


@router.get("/authentication_test")
def test_authorization(user: Json = Depends(get_current_user)) -> dict:
    """
    Returns the user, if authenticated correctly.
    """
    return {"msg": "success", "user": user}
