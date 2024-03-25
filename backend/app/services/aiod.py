from enum import Enum
from pathlib import Path
from urllib.parse import urljoin

from fastapi import HTTPException
from httpx import AsyncClient
from pydantic import Json

from app.config import settings
from app.helpers import Pagination


class AssetType(Enum):
    DATASETS: str = "datasets"
    ML_MODELS: str = "ml_models"
    PUBLICATIONS: str = "publications"
    PLATFORMS: str = "platforms"


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
