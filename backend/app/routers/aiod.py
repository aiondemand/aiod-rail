from pathlib import Path
from typing import Any
from urllib.parse import urljoin

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from pydantic import Json

from app.authentication import get_current_user, get_current_user_token
from app.config import settings
from app.helpers import Pagination, aiod_client_wrapper
from app.schemas.dataset import Dataset
from app.schemas.ml_model import MLModel
from app.schemas.platform import Platform
from app.schemas.publication import Publication

router = APIRouter()


@router.get("/secure-endpoint/")
async def secure_endpoint(current_user: dict = Depends(get_current_user)):
    # Use the authenticated user information
    return {"user": current_user}


""" Datasets """


@router.get("/datasets", response_model=list[Dataset])
async def get_datasets(pagination: Pagination = Depends()) -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path("datasets", settings.AIOD_API.DATASETS_VERSION).as_posix(),
        ),
        params={"offset": pagination.offset, "limit": pagination.limit},
    )
    return res.json()


@router.get("/datasets/search/{query}", response_model=list[Dataset])
async def search_datasets(query: str, pagination: Pagination = Depends()) -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path("search/datasets", settings.AIOD_API.DATASETS_VERSION).as_posix(),
        ),
        params={
            "search_query": query,
            "search_fields": "name",
            "limit": pagination.limit,
            "offset": pagination.offset,
            "get_all": True,
        },
    )
    return res.json()["resources"]


@router.get("/datasets/{id}", response_model=Dataset)
async def get_dataset(id: int) -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path(
                "datasets", settings.AIOD_API.DATASETS_VERSION, str(id)
            ).as_posix(),
        ),
    )
    return res.json()


@router.get("/counts/datasets", response_model=int)
async def get_datasets_count() -> Any:
    async_client = aiod_client_wrapper()

    res = await async_client.get(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path("counts/datasets", settings.AIOD_API.DATASETS_VERSION).as_posix(),
        ),
    )
    return res.json()


@router.get("/counts/datasets/search/{query}", response_model=int)
async def get_filtered_datasets_count(query: str) -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path("search/datasets", settings.AIOD_API.DATASETS_VERSION).as_posix(),
        ),
        params={"search_query": query, "search_fields": "name", "limit": 1},
    )
    return res.json()["total_hits"]


@router.post("/datasets", response_model=Dataset)
async def create_dataset(
    dataset: Dataset,
    token: str = Depends(get_current_user_token),
    user: Json = Depends(get_current_user),
) -> Any:
    async_client = aiod_client_wrapper()
    # Create a new dataset in AIoD (just metadata)
    res = await async_client.post(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path("datasets", settings.AIOD_API.DATASETS_VERSION).as_posix(),
        ),
        headers={"Authorization": f"{token}"},
        json=dataset.dict(exclude_unset=True),
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
async def delete_dataset(id: int, token: str = Depends(get_current_user_token)) -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.delete(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path(
                "datasets", settings.AIOD_API.DATASETS_VERSION, str(id)
            ).as_posix(),
        ),
        headers={"Authorization": f"{token}"},
    )

    if res.status_code != 200:
        print("ERROR", res.json())
        raise HTTPException(
            status_code=res.status_code,
            detail=f"Failed to delete dataset on AIoD. {res.json()}",
        )

    return True


@router.post("/datasets/{id}/upload-file-to-huggingface", response_model=Dataset)
async def dataset_upload_file_to_huggingface(
    id: int,
    file: UploadFile,
    huggingface_name: str,
    huggingface_token: str,
    token: str = Depends(get_current_user_token),
) -> Any:
    async_client = aiod_client_wrapper()

    res = await async_client.post(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path("upload/datasets", str(id), "huggingface").as_posix(),
        ),
        params={"token": huggingface_token, "username": huggingface_name},
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


async def get_dataset_name(id: int) -> str:
    dataset = Dataset(**await get_dataset(id))
    return dataset.name


""" ML Models """


@router.get("/models", response_model=list[MLModel])
async def get_models(pagination: Pagination = Depends()) -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path("ml_models", settings.AIOD_API.ML_MODELS_VERSION).as_posix(),
        ),
        params={"offset": pagination.offset, "limit": pagination.limit},
    )
    return res.json()


@router.get("/models/search/{query}", response_model=list[MLModel])
async def search_models(query: str, pagination: Pagination = Depends()) -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path(
                "search/ml_models", settings.AIOD_API.ML_MODELS_VERSION
            ).as_posix(),
        ),
        params={
            "search_query": query,
            "search_fields": "name",
            "limit": pagination.limit,
            "offset": pagination.offset,
            "get_all": True,
        },
    )
    return res.json()["resources"]


@router.get("/models/{id}", response_model=MLModel)
async def get_model(id: int) -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path(
                "ml_models", settings.AIOD_API.ML_MODELS_VERSION, str(id)
            ).as_posix(),
        ),
    )
    return res.json()


@router.get("/counts/models", response_model=int)
async def get_models_count() -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path(
                "counts/ml_models", settings.AIOD_API.ML_MODELS_VERSION
            ).as_posix(),
        ),
    )
    return res.json()


@router.get("/counts/models/search/{query}", response_model=int)
async def get_filtered_models_count(query: str) -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path(
                "search/ml_models", settings.AIOD_API.ML_MODELS_VERSION
            ).as_posix(),
        ),
        params={"search_query": query, "search_fields": "name", "limit": 1},
    )
    return res.json()["total_hits"]


async def get_model_name(id: int) -> str:
    ml_model = MLModel(**await get_model(id))
    return ml_model.name


""" Publications """


@router.get("/publications", response_model=list[Publication])
async def get_publications(pagination: Pagination = Depends()) -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path("publications", settings.AIOD_API.PUBLICATIONS_VERSION).as_posix(),
        ),
        params={"offset": pagination.offset, "limit": pagination.limit},
    )
    return res.json()


@router.get("/publications/search/{query}", response_model=list[Publication])
async def search_publications(query: str, pagination: Pagination = Depends()) -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path(
                "search/publications", settings.AIOD_API.PUBLICATIONS_VERSION
            ).as_posix(),
        ),
        params={
            "search_query": query,
            "search_fields": "name",
            "limit": pagination.limit,
            "offset": pagination.offset,
            "get_all": True,
        },
    )
    return res.json()["resources"]


@router.get("/publications/{id}", response_model=Publication)
async def get_publication(id: int) -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path(
                "publications", settings.AIOD_API.PUBLICATIONS_VERSION, str(id)
            ).as_posix(),
        ),
    )
    return res.json()


@router.get("/counts/publications", response_model=int)
async def get_publications_count() -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path(
                "counts/publications", settings.AIOD_API.PUBLICATIONS_VERSION
            ).as_posix(),
        ),
    )
    return res.json()


@router.get("/counts/publications/search/{query}", response_model=int)
async def get_filtered_publications_count(query: str) -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path(
                "search/publications", settings.AIOD_API.PUBLICATIONS_VERSION
            ).as_posix(),
        ),
        params={"search_query": query, "search_fields": "name", "limit": 1},
    )
    return res.json()["total_hits"]


@router.get("/platforms", response_model=list[Platform])
async def get_platforms() -> Any:
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path("platforms", settings.AIOD_API.PLATFORMS_VERSION).as_posix(),
        ),
    )

    if res.status_code != 200:
        raise HTTPException(
            status_code=res.status_code,
            detail=f"Failed to get platforms from AIoD. {res.json()}",
        )

    return res.json()
