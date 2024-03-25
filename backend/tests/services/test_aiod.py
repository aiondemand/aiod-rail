from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import HTTPException

from app.helpers import Pagination
from app.services.aiod import (
    AssetType,
    get_asset,
    get_assets,
    get_assets_count,
    search_assets,
)


@pytest.mark.parametrize(
    "asset_type, expected_url",
    [
        (AssetType.DATASETS, "https://api.aiod.eu/datasets/v0"),
        (AssetType.ML_MODELS, "https://api.aiod.eu/ml_models/v1"),
        (AssetType.PUBLICATIONS, "https://api.aiod.eu/publications/v2"),
        (AssetType.PLATFORMS, "https://api.aiod.eu/platforms/v3"),
    ],
)
@pytest.mark.asyncio
async def test_get_assets_happy_path(asset_type, expected_url):
    mock_response = Mock()
    mock_response.status_code = 200

    async with AsyncMock() as async_client_mock:
        async_client_mock.get.return_value = mock_response

        _ = await get_assets(async_client_mock, asset_type, pagination=Pagination())

        async_client_mock.get.assert_called_once_with(
            expected_url, params=Pagination().dict()
        )


@pytest.mark.parametrize("asset_type", list(AssetType))
@pytest.mark.asyncio
async def test_get_assets_raises_exception_on_non_200_status_code(asset_type):
    mock_response = Mock()
    mock_response.status_code = 404

    async with AsyncMock() as async_client_mock:
        async_client_mock.get.return_value = mock_response

        with pytest.raises(HTTPException):
            await get_assets(async_client_mock, asset_type, Pagination())


@pytest.mark.parametrize(
    "asset_type, expected_url",
    [
        (AssetType.DATASETS, "https://api.aiod.eu/datasets/v0"),
        (AssetType.ML_MODELS, "https://api.aiod.eu/ml_models/v1"),
        (AssetType.PUBLICATIONS, "https://api.aiod.eu/publications/v2"),
    ],
)
@pytest.mark.asyncio
async def test_get_asset_happy_path(asset_type, expected_url):
    mock_response = Mock()
    mock_response.status_code = 200

    async with AsyncMock() as async_client_mock:
        async_client_mock.get.return_value = mock_response

        _ = await get_asset(async_client_mock, asset_type, asset_id=42)

        async_client_mock.get.assert_called_once_with(f"{expected_url}/42")


@pytest.mark.parametrize("asset_type", list(AssetType))
@pytest.mark.asyncio
async def test_get_asset_raises_exception_on_non_200_status_code(asset_type):
    mock_response = Mock()
    mock_response.status_code = 404

    async with AsyncMock() as async_client_mock:
        async_client_mock.get.return_value = mock_response

        with pytest.raises(HTTPException):
            await get_asset(async_client_mock, asset_type, asset_id=42)


@pytest.mark.parametrize(
    "asset_type, expected_url",
    [
        (AssetType.DATASETS, "https://api.aiod.eu/counts/datasets/v0"),
        (AssetType.ML_MODELS, "https://api.aiod.eu/counts/ml_models/v1"),
        (AssetType.PUBLICATIONS, "https://api.aiod.eu/counts/publications/v2"),
        (AssetType.PLATFORMS, "https://api.aiod.eu/counts/platforms/v3"),
    ],
)
@pytest.mark.asyncio
async def test_get_assets_count_happy_path(asset_type, expected_url):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = 123

    async with AsyncMock() as async_client_mock:
        async_client_mock.get.return_value = mock_response

        res_counts = await get_assets_count(async_client_mock, asset_type)

        async_client_mock.get.assert_called_once_with(expected_url)
        assert res_counts == 123


@pytest.mark.parametrize(
    "asset_type, expected_url",
    [
        (AssetType.DATASETS, "https://api.aiod.eu/search/datasets/v0"),
        (AssetType.ML_MODELS, "https://api.aiod.eu/search/ml_models/v1"),
        (AssetType.PUBLICATIONS, "https://api.aiod.eu/search/publications/v2"),
    ],
)
@pytest.mark.asyncio
async def test_get_assets_count_with_query_happy_path(asset_type, expected_url):
    query = "asset_name"
    mock_search_response = {
        "total_hits": 1,
        "resources": [{"name": "asset_name_1"}],
        "offset": 0,
        "limit": 1,
    }
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_search_response

    async with AsyncMock() as async_client_mock:
        async_client_mock.get.return_value = mock_response

        res_counts = await get_assets_count(
            async_client_mock, asset_type, filter_query=query
        )

        async_client_mock.get.assert_called_once_with(
            expected_url,
            params={
                "search_query": query,
                "search_fields": "name",
                "limit": 1,
                "get_all": False,
            },
        )
        assert res_counts == mock_search_response["total_hits"]


@pytest.mark.parametrize("asset_type", list(AssetType))
@pytest.mark.asyncio
async def test_get_assets_count_raises_exception_on_non_200_status_code(asset_type):
    mock_response = Mock()
    mock_response.status_code = 404

    async with AsyncMock() as async_client_mock:
        async_client_mock.get.return_value = mock_response

        with pytest.raises(HTTPException):
            await get_assets_count(async_client_mock, asset_type)


@pytest.mark.parametrize(
    "asset_type, expected_url",
    [
        (AssetType.DATASETS, "https://api.aiod.eu/search/datasets/v0"),
        (AssetType.ML_MODELS, "https://api.aiod.eu/search/ml_models/v1"),
        (AssetType.PUBLICATIONS, "https://api.aiod.eu/search/publications/v2"),
    ],
)
@pytest.mark.asyncio
async def test_search_assets_happy_path(asset_type, expected_url):
    query = "asset_name"
    pagination = Pagination(offset=7, limit=13)
    mock_search_response = {
        "total_hits": 1,
        "resources": [{"name": "asset_name_1"}],
        "offset": 7,
        "limit": 13,
    }
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_search_response

    async with AsyncMock() as async_client_mock:
        async_client_mock.get.return_value = mock_response

        res_resources = await search_assets(
            async_client_mock, asset_type, query, pagination
        )

        async_client_mock.get.assert_called_once_with(
            expected_url,
            params={
                "search_query": query,
                "search_fields": "name",
                "offset": pagination.offset,
                "limit": pagination.limit,
                "get_all": True,
            },
        )
        assert res_resources == mock_search_response["resources"]


@pytest.mark.parametrize(
    "asset_type", [AssetType.DATASETS, AssetType.ML_MODELS, AssetType.PUBLICATIONS]
)
@pytest.mark.asyncio
async def test_search_assets_raises_exception_on_non_200_status_code(asset_type):
    mock_response = Mock()
    mock_response.status_code = 404

    async with AsyncMock() as async_client_mock:
        async_client_mock.get.return_value = mock_response

        with pytest.raises(HTTPException):
            await search_assets(async_client_mock, asset_type, "", Pagination())
