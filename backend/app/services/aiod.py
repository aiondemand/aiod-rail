import asyncio
from enum import Enum
from pathlib import Path
from typing import List

import httpx
from fastapi import HTTPException
from pydantic import Json

from app.auth import _get_user
from app.config import settings
from app.helpers import Pagination
from app.schemas.asset_id import AssetId
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
aiod_library_client_wrapper = AsyncClientWrapper(base_url=settings.AIOD_LIBRARY_API.BASE_URL)
aiod_enhanced_search_client_wrapper = AsyncClientWrapper(
    base_url=settings.AIOD_ENHANCED_SEARCH_API.BASE_URL
)


async def get_assets(asset_type: AssetType, pagination: Pagination) -> list:
    """Wrapper function to call the AIoD API and return a list of requested assets."""
    res = await aiod_client_wrapper.client.get(
        Path(asset_type.value).as_posix(),
        params={"offset": pagination.offset, "limit": pagination.limit},
    )

    if res.status_code != 200:
        raise HTTPException(
            status_code=res.status_code,
            detail=f"Failed to get {asset_type.value} from AIoD. {res.json()}",
        )

    return res.json()


async def get_my_assets(asset_type: AssetType, token: str, pagination: Pagination) -> List[Json]:
    """Wrapper function to fetch my assets from AIoD's My Library."""
    my_asset_ids = await get_my_asset_ids(asset_type, token, pagination)
    my_assets = [
        await get_asset(asset_type=asset_type, asset_id=asset_id) for asset_id in my_asset_ids
    ]
    return my_assets


async def get_my_asset_ids(
    asset_type: AssetType, token: str, pagination: Pagination
) -> List[AssetId]:
    """Wrapper function to call the AIoD's My Library and return a list of identifiers of my requested assets.

    Pagination is currently not supported by My Library, so the behavior is just mimicked.

    Note: Only Datasets and ML_Models are supported currently.
    """
    assert asset_type in [AssetType.DATASETS, AssetType.ML_MODELS]

    user = await _get_user(token=token)
    user_id = user.get("sub")

    res = await aiod_library_client_wrapper.client.get(
        f"api/libraries/{user_id}/assets", headers={"Authorization": f"{token}"}
    )

    if res.status_code != 200:
        raise HTTPException(
            status_code=res.status_code,
            detail=f"Failed to get my {asset_type.value} from AIoD Library. {res.json()}",
        )

    # Currently, the API returns code: 404 IN RESPONSE if user has no library
    if res.json().get("code") == 404 or "data" not in res.json():
        raise HTTPException(
            status_code=404,
            detail=f"User does not have a library: {res.json()}",
        )
    else:
        my_assets = res.json().get("data", [])

    asset_name_mapper = {
        AssetType.DATASETS: "Dataset",
        AssetType.ML_MODELS: "AIModel",
    }

    requested_assets = [
        asset["identifier"]
        for asset in my_assets
        if asset["category"] == asset_name_mapper[asset_type]
    ]

    return requested_assets[pagination.offset : pagination.offset + pagination.limit]


async def get_asset(asset_type: AssetType, asset_id: AssetId) -> Json:
    """Wrapper function to call the AIoD API and return requested asset data."""
    res = await aiod_client_wrapper.client.get(
        Path(asset_type.value, asset_id).as_posix(),
    )

    if res.status_code != 200:
        raise HTTPException(
            status_code=res.status_code,
            detail=f"Failed to get {asset_type.value} from AIoD. {res.json()}",
        )

    return res.json()


async def get_assets_count(asset_type: AssetType, filter_query: str | None = None) -> int:
    """Wrapper function to call the AIoD API and return the total counts of requested assets.

    Note: The current AIoD API 'counts' endpoint does not support filtering of assets to count.
    Therefore, the desired logic is achieved by calling the 'search' endpoint in that case.
    """
    if filter_query is None:
        res = await aiod_client_wrapper.client.get(
            Path(f"counts/{asset_type.value}").as_posix(),
        )
    else:
        res = await aiod_client_wrapper.client.get(
            Path(
                f"search/{asset_type.value}",
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


async def search_assets(asset_type: AssetType, query: str, pagination: Pagination) -> list:
    """Wrapper function to call the AIoD API and return a list of requested assets."""
    res = await aiod_client_wrapper.client.get(
        Path(f"search/{asset_type.value}").as_posix(),
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


async def enhanced_search(asset_type: AssetType, query: str, pagination: Pagination) -> list:
    topk = min(pagination.offset + pagination.limit, 100)
    initial_response = await aiod_enhanced_search_client_wrapper.client.post(
        "query",
        params={"search_query": query, "asset_type": asset_type.value, "topk": topk},
    )

    if initial_response.status_code != 202:
        raise HTTPException(
            status_code=initial_response.status_code, detail="Failed to initiate query"
        )

    # Extract the location header to poll for results
    result_location = initial_response.headers.get("location")
    if not result_location:
        raise HTTPException(
            status_code=500, detail="Missing Location header in external API response"
        )

    # Poll the result endpoint until we get the result
    max_retries = 5 + round(topk * 0.15)
    delay = 2
    for _ in range(max_retries):
        result_response: httpx.Response = await aiod_enhanced_search_client_wrapper.client.get(
            result_location,
            params={"return_entire_assets": True},
            follow_redirects=True,
        )
        if result_response.status_code == 200 and result_response.json()["status"] == "Completed":
            results = result_response.json()["results"][-pagination.limit :]
            assets = [result["asset"] for result in results]
            return assets

        elif result_response.status_code == 200:
            await asyncio.sleep(delay)
        else:
            raise HTTPException(
                status_code=result_response.status_code, detail="Error fetching results"
            )

    raise HTTPException(status_code=504, detail="Timed out waiting for result from external API")


async def get_dataset_name(id: AssetId) -> str:
    """Helper function to fetch requested Dataset and return its name"""
    dataset = Dataset(**await get_asset(asset_type=AssetType.DATASETS, asset_id=id))
    return dataset.name


async def get_model_name(id: AssetId) -> str:
    """Helper function to fetch requested MLModel and return its name"""
    ml_model = MLModel(**await get_asset(asset_type=AssetType.ML_MODELS, asset_id=id))
    return ml_model.name
