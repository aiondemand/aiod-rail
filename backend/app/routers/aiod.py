from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response, UploadFile, status

from app.auth import get_current_user, get_current_user_token
from app.config import settings
from app.helpers import Pagination
from app.schemas.dataset import Dataset
from app.schemas.ml_model import MLModel
from app.schemas.platform import Platform
from app.schemas.publication import Publication
from app.services.aiod import (
    AssetType,
    aiod_client_wrapper,
    enhanced_search,
    get_asset,
    get_assets,
    get_assets_count,
    get_assets_version,
    get_my_asset_ids,
    get_my_assets,
    search_assets,
)

router = APIRouter()

""" Datasets """


@router.get("/datasets", response_model=list[Dataset])
async def get_datasets(pagination: Pagination = Depends()) -> Any:
    return await get_assets(asset_type=AssetType.DATASETS, pagination=pagination)


@router.get("/datasets/my", response_model=list[Dataset])
async def get_my_datasets(
    response: Response,
    token: str = Depends(get_current_user_token),
    pagination: Pagination = Depends(),
) -> Any:
    try:
        return await get_my_assets(
            asset_type=AssetType.DATASETS, token=token, pagination=pagination
        )
    except HTTPException as e:
        if e.status_code == 404:
            response.status_code = status.HTTP_204_NO_CONTENT
            return []
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to get my datasets.",
        )


@router.get("/datasets/search/{query}", response_model=list[Dataset])
async def search_datasets(
    query: str, enhanced: bool = False, pagination: Pagination = Depends()
) -> Any:
    if not enhanced:
        return await search_assets(
            asset_type=AssetType.DATASETS,
            query=query,
            pagination=pagination,
        )
    else:
        return await enhanced_search(
            asset_type=AssetType.DATASETS,
            query=query,
            pagination=pagination,
        )


@router.get("/datasets/{id}", response_model=Dataset)
async def get_dataset(id: int) -> Any:
    return await get_asset(asset_type=AssetType.DATASETS, asset_id=id)


@router.get("/counts/datasets", response_model=int)
async def get_datasets_count() -> Any:
    return await get_assets_count(asset_type=AssetType.DATASETS)


@router.get("/counts/datasets/search/{query}", response_model=int)
async def get_filtered_datasets_count(query: str) -> Any:
    return await get_assets_count(asset_type=AssetType.DATASETS, filter_query=query)


@router.get("/counts/datasets/my", response_model=int)
async def get_my_datasets_count(
    response: Response, token: str = Depends(get_current_user_token)
) -> Any:
    try:
        my_dataset_ids = await get_my_asset_ids(
            AssetType.DATASETS, token, Pagination(offset=0, limit=10e10)
        )
        return len(my_dataset_ids)
    except HTTPException as e:
        if e.status_code == 404:
            response.status_code = status.HTTP_204_NO_CONTENT
            return 0
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to get my datasets count.",
        )


@router.post(
    "/datasets",
    dependencies=[Depends(get_current_user(required=True, from_api_key=False))],
    response_model=Dataset,
)
async def create_dataset(
    dataset: Dataset,
    token: str = Depends(get_current_user_token),
) -> Any:
    # Create a new dataset in AIoD (just metadata)
    res = await aiod_client_wrapper.client.post(
        Path(AssetType.DATASETS.value, get_assets_version(AssetType.DATASETS)),
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
    res = await aiod_client_wrapper.client.delete(
        Path("datasets", settings.AIOD_API.DATASETS_VERSION, str(id)),
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
    res = await aiod_client_wrapper.client.post(
        Path("upload/datasets", str(id), "huggingface"),
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


""" ML Models """


@router.get("/models", response_model=list[MLModel])
async def get_models(pagination: Pagination = Depends()) -> Any:
    return await get_assets(asset_type=AssetType.ML_MODELS, pagination=pagination)


@router.get("/models/my", response_model=list[MLModel])
async def get_my_models(
    response: Response,
    token: str = Depends(get_current_user_token),
    pagination: Pagination = Depends(),
) -> Any:
    try:
        return await get_my_assets(
            asset_type=AssetType.ML_MODELS, token=token, pagination=pagination
        )
    except HTTPException as e:
        if e.status_code == 404:
            response.status_code = status.HTTP_204_NO_CONTENT
            return []
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to get my models.",
        )


@router.get("/models/search/{query}", response_model=list[MLModel])
async def search_models(query: str, pagination: Pagination = Depends()) -> Any:
    return await search_assets(
        asset_type=AssetType.ML_MODELS,
        query=query,
        pagination=pagination,
    )


@router.get("/models/{id}", response_model=MLModel)
async def get_model(id: int) -> Any:
    return await get_asset(asset_type=AssetType.ML_MODELS, asset_id=id)


@router.get("/counts/models", response_model=int)
async def get_models_count() -> Any:
    return await get_assets_count(asset_type=AssetType.ML_MODELS)


@router.get("/counts/models/my", response_model=int)
async def get_my_models_count(
    response: Response, token: str = Depends(get_current_user_token)
) -> Any:
    try:
        my_dataset_ids = await get_my_asset_ids(
            AssetType.ML_MODELS, token, Pagination(offset=0, limit=10e10)
        )
        return len(my_dataset_ids)
    except HTTPException as e:
        if e.status_code == 404:
            response.status_code = status.HTTP_204_NO_CONTENT
            return 0
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to get my models count.",
        )


@router.get("/counts/models/search/{query}", response_model=int)
async def get_filtered_models_count(query: str) -> Any:
    return await get_assets_count(asset_type=AssetType.ML_MODELS, filter_query=query)


""" Publications """


@router.get("/publications", response_model=list[Publication])
async def get_publications(pagination: Pagination = Depends()) -> Any:
    return await get_assets(asset_type=AssetType.PUBLICATIONS, pagination=pagination)


@router.get("/publications/search/{query}", response_model=list[Publication])
async def search_publications(query: str, pagination: Pagination = Depends()) -> Any:
    return await search_assets(
        asset_type=AssetType.PUBLICATIONS,
        query=query,
        pagination=pagination,
    )


@router.get("/publications/{id}", response_model=Publication)
async def get_publication(id: int) -> Any:
    return await get_asset(asset_type=AssetType.PUBLICATIONS, asset_id=id)


@router.get("/counts/publications", response_model=int)
async def get_publications_count() -> Any:
    return await get_assets_count(asset_type=AssetType.PUBLICATIONS)


@router.get("/counts/publications/search/{query}", response_model=int)
async def get_filtered_publications_count(query: str) -> Any:
    return await get_assets_count(asset_type=AssetType.PUBLICATIONS, filter_query=query)


@router.get("/platforms", response_model=list[Platform])
async def get_platforms(pagination: Pagination = Depends()) -> Any:
    return await get_assets(asset_type=AssetType.PLATFORMS, pagination=pagination)
