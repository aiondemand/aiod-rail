from enum import Enum
from pathlib import Path
from typing import List

import httpx
from fastapi import HTTPException
from pydantic import Json

from app.config import settings
from app.helpers import Pagination
from app.schemas.dataset import Dataset
from app.schemas.ml_model import MLModel


class AssetType(Enum):
    DATASETS: str = "datasets"
    ML_MODELS: str = "ml_models"
    PUBLICATIONS: str = "publications"
    PLATFORMS: str = "platforms"


class AsyncClientWrapper:
    def __init__(self, base_url: str):
        self.async_client = None
        self.base_url = base_url

    def start(self):
        """Instantiate the client. Call from the FastAPI startup hook."""
        self.async_client = httpx.AsyncClient(base_url=self.base_url)

    async def stop(self):
        """Gracefully shutdown. Call from FastAPI shutdown hook."""
        await self.async_client.aclose()
        self.async_client = None

    @property
    def client(self):
        assert self.async_client is not None
        return self.async_client


aiod_client_wrapper = AsyncClientWrapper(base_url=settings.AIOD_API.BASE_URL)
aiod_library_client_wrapper = AsyncClientWrapper(
    base_url=settings.AIOD_LIBRARY_API.BASE_URL
)


def get_assets_version(asset_type: AssetType) -> str:
    match asset_type:
        case AssetType.DATASETS:
            return settings.AIOD_API.DATASETS_VERSION
        case AssetType.ML_MODELS:
            return settings.AIOD_API.ML_MODELS_VERSION
        case AssetType.PUBLICATIONS:
            return settings.AIOD_API.PUBLICATIONS_VERSION
        case AssetType.PLATFORMS:
            return settings.AIOD_API.PLATFORMS_VERSION


async def get_assets(asset_type: AssetType, pagination: Pagination) -> list:
    """Wrapper function to call the AIoD API and return a list of requested assets."""
    res = await aiod_client_wrapper.client.get(
        Path(asset_type.value, get_assets_version(asset_type)).as_posix(),
        params={"offset": pagination.offset, "limit": pagination.limit},
    )

    if res.status_code != 200:
        raise HTTPException(
            status_code=res.status_code,
            detail=f"Failed to get {asset_type.value} from AIoD. {res.json()}",
        )

    return res.json()


async def get_my_assets(asset_type: AssetType, user_id: str, token: str) -> List[Json]:
    """Wrapper function to fetch my assets from AIoD's My Library."""
    my_asset_ids = await get_my_asset_ids(asset_type, user_id, token)
    my_assets = [
        await get_asset(asset_type=asset_type, asset_id=asset_id)
        for asset_id in my_asset_ids
    ]
    return my_assets


async def get_my_asset_ids(
    asset_type: AssetType, user_id: str, token: str
) -> List[int]:
    """Wrapper function to call the AIoD's My Library and return a list of identifiers of my requested assets.

    Note: Only Datasets and ML_Models are supported currently.
    """
    assert asset_type in [AssetType.DATASETS, AssetType.ML_MODELS]

    res = await aiod_library_client_wrapper.client.get(
        f"api/libraries/{user_id}/assets", headers={"Authorization": f"{token}"}
    )

    if res.status_code != 200:
        raise HTTPException(
            status_code=res.status_code,
            detail=f"Failed to get my {asset_type.value} from AIoD Library. {res.json()}",
        )

    asset_name_mapper = {
        AssetType.DATASETS: "Dataset",
        AssetType.ML_MODELS: "AIModel",
    }

    requested_assets = [
        int(asset["identifier"])
        for asset in res.json()["data"]
        if asset["category"] == asset_name_mapper[asset_type]
    ]

    return requested_assets


async def get_asset(asset_type: AssetType, asset_id: int) -> Json:
    """Wrapper function to call the AIoD API and return requested asset data."""
    res = await aiod_client_wrapper.client.get(
        Path(
            asset_type.value, get_assets_version(asset_type), str(asset_id)
        ).as_posix(),
    )

    if res.status_code != 200:
        raise HTTPException(
            status_code=res.status_code,
            detail=f"Failed to get {asset_type.value} from AIoD. {res.json()}",
        )

    return res.json()


async def get_assets_count(asset_type: AssetType, filter_query: str = None) -> int:
    """Wrapper function to call the AIoD API and return the total counts of requested assets.

    Note: The current AIoD API 'counts' endpoint does not support filtering of assets to count.
    Therefore, the desired logic is achieved by calling the 'search' endpoint in that case.
    """
    if filter_query is None:
        res = await aiod_client_wrapper.client.get(
            Path(
                f"counts/{asset_type.value}", get_assets_version(asset_type)
            ).as_posix(),
        )
    else:
        res = await aiod_client_wrapper.client.get(
            Path(
                f"search/{asset_type.value}", get_assets_version(asset_type)
            ).as_posix(),
            params={
                "search_query": filter_query,
                "search_fields": "name",
                "limit": 1,
                "get_all": False,
            },
        )

    if res.status_code != 200:
        raise HTTPException(
            status_code=res.status_code,
            detail=f"Failed to get counts for {asset_type.value} from AIoD. {res.json()}",
        )
    elif filter_query is None:
        return res.json()
    else:
        return res.json()["total_hits"]


async def search_assets(
    asset_type: AssetType, query: str, pagination: Pagination
) -> list:
    """Wrapper function to call the AIoD API and return a list of requested assets."""
    res = await aiod_client_wrapper.client.get(
        Path(f"search/{asset_type.value}", get_assets_version(asset_type)).as_posix(),
        params={
            "search_query": query,
            "search_fields": "name",
            "offset": pagination.offset,
            "limit": pagination.limit,
            "get_all": True,
        },
    )

    if res.status_code != 200:
        raise HTTPException(
            status_code=res.status_code,
            detail=f"Failed to search {asset_type.value} from AIoD. {res.json()}",
        )

    return res.json()["resources"]


async def get_dataset_name(id: int) -> str:
    """Helper function to fetch requested Dataset and return its name"""
    dataset = Dataset(**await get_asset(asset_type=AssetType.DATASETS, asset_id=id))
    return dataset.name


async def get_model_name(id: int) -> str:
    """Helper function to fetch requested MLModel and return its name"""
    ml_model = MLModel(**await get_asset(asset_type=AssetType.ML_MODELS, asset_id=id))
    return ml_model.name
