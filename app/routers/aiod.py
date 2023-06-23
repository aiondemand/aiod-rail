from typing import Any

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from pydantic import Json

from app.authentication import get_current_user, get_current_uset_token
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


@router.post("/datasets", response_model=Dataset)
async def create_dataset(
    dataset: Dataset,
    token: str = Depends(get_current_uset_token),
    user: Json = Depends(get_current_user),
) -> Any:
    async_client = aiod_client_wrapper()
    # Create a new dataset in AIoD (just metadata)
    res = await async_client.post(
        f"{settings.AIOD_API.BASE_URL}/datasets/{settings.AIOD_API.DATASETS_VERSION}",
        headers={"Authorization": f"{token}"},
        json=dataset.dict(),
    )

    if res.status_code != 200:
        raise HTTPException(
            status_code=res.status_code,
            detail=f"Failed to create the dataset on AIoD. {res.json()}",
        )

    # As the API only returns the ID of the new dataset as {identifier: id},
    # we need to fetch it again
    new_dataset_id = res.json()["identifier"]
    dataset = await get_dataset(new_dataset_id)

    return dataset


@router.delete("/datasets/{id}", response_model=bool)
async def delete_dataset(id: int, token: str = Depends(get_current_uset_token)) -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.delete(
        f"{settings.AIOD_API.BASE_URL}/datasets/{settings.AIOD_API.DATASETS_VERSION}/{id}",
        headers={"Authorization": f"{token}"},
    )

    if res.status_code != 200:
        print("ERROR", res.json())
        raise HTTPException(
            status_code=res.status_code,
            detail=f"Failed to delete dataset on AIoD. {res.json()}",
        )

    return True


@router.post("/datasets/{id}/upload-file", response_model=Dataset)
async def dataset_upload_file(
    id: int,
    file: UploadFile,
    huggingface_name: str,
    huggingface_token: str,
    token: str = Depends(get_current_uset_token),
) -> Any:
    async_client = aiod_client_wrapper()

    res = await async_client.post(
        f"{settings.AIOD_API.BASE_URL}/upload/datasets/{id}/huggingface?token={huggingface_token}&username={huggingface_name}",
        headers={"Authorization": f"{token}"},
        files={"file": (file.filename, file.file, file.content_type)},
    )

    if res.status_code != 200:
        print(f"Failed to upload the file to HuggingFace. {res.json()}")
        raise HTTPException(
            status_code=res.status_code,
            detail=f"Failed to upload the file to HuggingFace. {res.json()}",
        )

    # As the API only returns the ID as integer of the new dataset,
    # we need to fetch it again
    new_dataset_id = res.json()
    dataset = await get_dataset(new_dataset_id)

    return dataset


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


@router.get("/platforms", response_model=list[str])
async def get_platforms() -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        f"{settings.AIOD_API.BASE_URL}/platforms/{settings.AIOD_API.PLATFORMS_VERSION}",
    )

    if res.status_code != 200:
        raise HTTPException(
            status_code=res.status_code,
            detail=f"Failed to get platforms from AIoD. {res.json()}",
        )

    return res.json()
