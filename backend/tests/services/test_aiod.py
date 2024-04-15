from unittest.mock import Mock, call

import pytest
from fastapi import HTTPException

from app.helpers import Pagination
from app.services.aiod import (
    AssetType,
    get_asset,
    get_assets,
    get_assets_count,
    get_my_asset_ids,
    get_my_assets,
    search_assets,
)


@pytest.mark.parametrize(
    "asset_type, expected_url",
    [
        (AssetType.DATASETS, "datasets/v0"),
        (AssetType.ML_MODELS, "ml_models/v1"),
        (AssetType.PUBLICATIONS, "publications/v2"),
        (AssetType.PLATFORMS, "platforms/v3"),
    ],
)
@pytest.mark.asyncio
async def test_get_assets_happy_path(asset_type, expected_url, async_client_mock):
    mock_response = Mock()
    mock_response.status_code = 200
    async_client_mock.get.return_value = mock_response

    _ = await get_assets(asset_type, pagination=Pagination())

    async_client_mock.get.assert_called_once_with(
        expected_url, params=Pagination().dict()
    )


@pytest.mark.parametrize("asset_type", list(AssetType))
@pytest.mark.asyncio
async def test_get_assets_raises_exception_on_non_200_status_code(
    asset_type, async_client_mock
):
    mock_response = Mock()
    mock_response.status_code = 404
    async_client_mock.get.return_value = mock_response

    with pytest.raises(HTTPException):
        await get_assets(asset_type, Pagination())


@pytest.mark.parametrize(
    "asset_type",
    [AssetType.DATASETS, AssetType.ML_MODELS],
)
@pytest.mark.asyncio
async def test_get_my_assets_happy_path(mocker, asset_type):
    mock_get_my_asset_ids = mocker.patch(
        "app.services.aiod.get_my_asset_ids", return_value=[1, 2, 3]
    )
    mock_get_asset = mocker.patch(
        "app.services.aiod.get_asset", return_value=[{}, {}, {}]
    )

    _ = await get_my_assets(asset_type, user_id="user-id", token="valid-user-token")

    mock_get_my_asset_ids.assert_called_with(asset_type, "user-id", "valid-user-token")
    assert mock_get_asset.mock_calls == [
        call(asset_type=asset_type, asset_id=1),
        call(asset_type=asset_type, asset_id=2),
        call(asset_type=asset_type, asset_id=3),
    ]


@pytest.mark.parametrize(
    "asset_type, expected_url, expected_asset_ids",
    [
        (AssetType.DATASETS, "api/libraries/{user_id}/assets", [1]),
        (AssetType.ML_MODELS, "api/libraries/{user_id}/assets", [14]),
    ],
)
@pytest.mark.asyncio
async def test_get_my_asset_ids_happy_path(
    asset_type, expected_url, expected_asset_ids, async_client_mock
):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [
            {
                "identifier": "14",
                "name": "kinit/slovakbert-sentiment-twitter",
                "category": "AIModel",
                "url_metadata": "https://huggingface.co/kinit/slovakbert-sentiment-twitter",
                "price": 0,
                "added_at": 30,
            },
            {
                "identifier": "1",
                "name": "acronym_identification",
                "category": "Dataset",
                "url_metadata": "https://huggingface.co/datasets/acronym_identification",
                "price": 0,
                "added_at": 15,
            },
        ],
        "code": 200,
    }
    async_client_mock.get.return_value = mock_response

    my_asset_ids = await get_my_asset_ids(
        asset_type, user_id="user-id", token="valid-user-token"
    )

    async_client_mock.get.assert_called_once_with(
        expected_url.format(user_id="user-id"),
        headers={"Authorization": "valid-user-token"},
    )

    assert isinstance(my_asset_ids, list)
    assert my_asset_ids == expected_asset_ids


@pytest.mark.parametrize("asset_type", [AssetType.DATASETS, AssetType.ML_MODELS])
@pytest.mark.asyncio
async def test_get_my_asset_ids_raises_exception_on_non_200_status_code(
    asset_type, async_client_mock
):
    mock_response = Mock()
    mock_response.status_code = 404
    async_client_mock.get.return_value = mock_response

    with pytest.raises(HTTPException):
        await get_my_asset_ids(asset_type, user_id="user-id", token="valid-user-token")


@pytest.mark.parametrize(
    "asset_type, expected_url",
    [
        (AssetType.DATASETS, "datasets/v0"),
        (AssetType.ML_MODELS, "ml_models/v1"),
        (AssetType.PUBLICATIONS, "publications/v2"),
    ],
)
@pytest.mark.asyncio
async def test_get_asset_happy_path(asset_type, expected_url, async_client_mock):
    mock_response = Mock()
    mock_response.status_code = 200
    async_client_mock.get.return_value = mock_response

    _ = await get_asset(asset_type, asset_id=42)

    async_client_mock.get.assert_called_once_with(f"{expected_url}/42")


@pytest.mark.parametrize("asset_type", list(AssetType))
@pytest.mark.asyncio
async def test_get_asset_raises_exception_on_non_200_status_code(
    asset_type, async_client_mock
):
    mock_response = Mock()
    mock_response.status_code = 404
    async_client_mock.get.return_value = mock_response

    with pytest.raises(HTTPException):
        await get_asset(asset_type, asset_id=42)


@pytest.mark.parametrize(
    "asset_type, expected_url",
    [
        (AssetType.DATASETS, "counts/datasets/v0"),
        (AssetType.ML_MODELS, "counts/ml_models/v1"),
        (AssetType.PUBLICATIONS, "counts/publications/v2"),
        (AssetType.PLATFORMS, "counts/platforms/v3"),
    ],
)
@pytest.mark.asyncio
async def test_get_assets_count_happy_path(asset_type, expected_url, async_client_mock):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = 123
    async_client_mock.get.return_value = mock_response

    res_counts = await get_assets_count(asset_type)

    async_client_mock.get.assert_called_once_with(expected_url)
    assert res_counts == 123


@pytest.mark.parametrize(
    "asset_type, expected_url",
    [
        (AssetType.DATASETS, "search/datasets/v0"),
        (AssetType.ML_MODELS, "search/ml_models/v1"),
        (AssetType.PUBLICATIONS, "search/publications/v2"),
    ],
)
@pytest.mark.asyncio
async def test_get_assets_count_with_query_happy_path(
    asset_type, expected_url, async_client_mock
):
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
    async_client_mock.get.return_value = mock_response

    res_counts = await get_assets_count(asset_type, filter_query=query)

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
async def test_get_assets_count_raises_exception_on_non_200_status_code(
    asset_type, async_client_mock
):
    mock_response = Mock()
    mock_response.status_code = 404
    async_client_mock.get.return_value = mock_response

    with pytest.raises(HTTPException):
        await get_assets_count(asset_type)


@pytest.mark.parametrize(
    "asset_type, expected_url",
    [
        (AssetType.DATASETS, "search/datasets/v0"),
        (AssetType.ML_MODELS, "search/ml_models/v1"),
        (AssetType.PUBLICATIONS, "search/publications/v2"),
    ],
)
@pytest.mark.asyncio
async def test_search_assets_happy_path(asset_type, expected_url, async_client_mock):
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
    async_client_mock.get.return_value = mock_response

    res_resources = await search_assets(asset_type, query, pagination)

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
async def test_search_assets_raises_exception_on_non_200_status_code(
    asset_type, async_client_mock
):
    mock_response = Mock()
    mock_response.status_code = 404
    async_client_mock.get.return_value = mock_response

    with pytest.raises(HTTPException):
        await search_assets(asset_type, "", Pagination())
