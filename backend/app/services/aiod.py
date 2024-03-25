from enum import Enum
from pathlib import Path
from urllib.parse import urljoin

import httpx
from fastapi import HTTPException
from httpx import AsyncClient
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


class AIoDClientWrapper:
    async_client = None

    def start(self):
        """Instantiate the client. Call from the FastAPI startup hook."""
        self.async_client = httpx.AsyncClient(verify=settings.AIOD_API.VERIFY_SSL)

    async def stop(self):
        """Gracefully shutdown. Call from FastAPI shutdown hook."""
        await self.async_client.aclose()
        self.async_client = None

    def __call__(self):
        """Calling the instantiated HTTPXClientWrapper returns the wrapped singleton."""
        assert self.async_client is not None
        return self.async_client


aiod_client_wrapper = AIoDClientWrapper()


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


async def get_assets(
    async_client: AsyncClient, asset_type: AssetType, pagination: Pagination
) -> list:
    res = await async_client.get(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path(asset_type.value, get_assets_version(asset_type)).as_posix(),
        ),
        params={"offset": pagination.offset, "limit": pagination.limit},
    )

    if res.status_code != 200:
        raise HTTPException(
            status_code=res.status_code,
            detail=f"Failed to get {asset_type.value} from AIoD. {res.json()}",
        )

    return res.json()


async def get_asset(
    async_client: AsyncClient, asset_type: AssetType, asset_id: int
) -> Json:
    res = await async_client.get(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path(
                asset_type.value, get_assets_version(asset_type), str(asset_id)
            ).as_posix(),
        ),
    )

    if res.status_code != 200:
        raise HTTPException(
            status_code=res.status_code,
            detail=f"Failed to get {asset_type.value} from AIoD. {res.json()}",
        )

    return res.json()


async def get_assets_count(
    async_client: AsyncClient, asset_type: AssetType, filter_query: str = None
) -> int:
    if filter_query is None:
        res = await async_client.get(
            urljoin(
                base=settings.AIOD_API.BASE_URL,
                url=Path(
                    f"counts/{asset_type.value}", get_assets_version(asset_type)
                ).as_posix(),
            ),
        )
    else:
        res = await async_client.get(
            urljoin(
                base=settings.AIOD_API.BASE_URL,
                url=Path(
                    f"search/{asset_type.value}", get_assets_version(asset_type)
                ).as_posix(),
            ),
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
    async_client: AsyncClient, asset_type: AssetType, query: str, pagination: Pagination
) -> list:
    res = await async_client.get(
        urljoin(
            base=settings.AIOD_API.BASE_URL,
            url=Path(
                f"search/{asset_type.value}", get_assets_version(asset_type)
            ).as_posix(),
        ),
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


async def get_dataset_name(async_client: AsyncClient, id: int) -> str:
    dataset = Dataset(
        **await get_asset(
            async_client=async_client, asset_type=AssetType.DATASETS, asset_id=id
        )
    )
    return dataset.name


async def get_model_name(async_client: AsyncClient, id: int) -> str:
    ml_model = MLModel(
        **await get_asset(
            async_client=async_client, asset_type=AssetType.ML_MODELS, asset_id=id
        )
    )
    return ml_model.name
