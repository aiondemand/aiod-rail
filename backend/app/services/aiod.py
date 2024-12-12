from enum import Enum
from pathlib import Path
from time import sleep
from typing import List

import httpx
from fastapi import HTTPException
from pydantic import Json

from app.auth import get_current_user
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
aiod_enhanced_search_client_wrapper = AsyncClientWrapper(
    base_url=settings.AIOD_ENHANCED_SEARCH_API.BASE_URL
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


async def get_my_assets(
    asset_type: AssetType, token: str, pagination: Pagination
) -> List[Json]:
    """Wrapper function to fetch my assets from AIoD's My Library."""
    my_asset_ids = await get_my_asset_ids(asset_type, token, pagination)
    my_assets = [
        await get_asset(asset_type=asset_type, asset_id=asset_id)
        for asset_id in my_asset_ids
    ]
    return my_assets


async def get_my_asset_ids(
    asset_type: AssetType, token: str, pagination: Pagination
) -> List[int]:
    """Wrapper function to call the AIoD's My Library and return a list of identifiers of my requested assets.

    Pagination is currently not supported by My Library, so the behavior is just mimicked.

    Note: Only Datasets and ML_Models are supported currently.
    """
    assert asset_type in [AssetType.DATASETS, AssetType.ML_MODELS]

    user = await get_current_user(required=True)(token=token)
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
        int(asset["identifier"])
        for asset in my_assets
        if asset["category"] == asset_name_mapper[asset_type]
    ]

    return requested_assets[pagination.offset : pagination.offset + pagination.limit]


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


async def enhanced_search(
    asset_type: AssetType, query: str, pagination: Pagination
) -> list:
    initial_response = await aiod_enhanced_search_client_wrapper.client.post(
        "query",
        params={
            "query": query,
            "asset_type": asset_type.value,
            # TODO: Update pagination
            "topk": min(pagination.offset + pagination.limit, 100),
        },
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
    max_retries = 10
    delay = 2
    for _ in range(max_retries):
        result_response: httpx.Response = (
            await aiod_enhanced_search_client_wrapper.client.get(
                result_location, follow_redirects=True
            )
        )

        if (
            result_response.status_code == 200
            and result_response.json()["status"] == "Completed"
        ):
            # TODO: Fix the type of response IDs
            asset_ids: list[str] = result_response.json()["result_doc_ids"]

            return [
                await get_asset(asset_type, int(asset_id))
                for asset_id in asset_ids[-pagination.limit :]
            ]
        elif result_response.status_code == 200:
            sleep(delay)
        else:
            raise HTTPException(
                status_code=result_response.status_code, detail="Error fetching results"
            )

    raise HTTPException(
        status_code=504, detail="Timed out waiting for result from external API"
    )


async def get_dataset_name(id: int) -> str:
    """Helper function to fetch requested Dataset and return its name"""
    dataset = Dataset(**await get_asset(asset_type=AssetType.DATASETS, asset_id=id))
    return dataset.name


async def get_model_name(id: int) -> str:
    """Helper function to fetch requested MLModel and return its name"""
    ml_model = MLModel(**await get_asset(asset_type=AssetType.ML_MODELS, asset_id=id))
    return ml_model.name
