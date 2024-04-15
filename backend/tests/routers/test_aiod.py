import pytest

from app.helpers import Pagination
from app.schemas.dataset import Dataset
from app.schemas.ml_model import MLModel
from app.schemas.platform import Platform
from app.schemas.publication import Publication
from app.services.aiod import AssetType


@pytest.mark.parametrize(
    "api_path, asset_type, asset_class",
    [
        ("/v1/assets/datasets", AssetType.DATASETS, Dataset),
        ("/v1/assets/models", AssetType.ML_MODELS, MLModel),
        ("/v1/assets/publications", AssetType.PUBLICATIONS, Publication),
        ("/v1/assets/platforms", AssetType.PLATFORMS, Platform),
    ],
)
@pytest.mark.asyncio
async def test_api_get_assets(client, mocker, api_path, asset_type, asset_class):
    pagination = Pagination(offset=7, limit=13)
    mock_get_assets = mocker.patch(
        "app.routers.aiod.get_assets",
        return_value=[{"name": "asset_name", "identifier": 42}],
    )

    res = client.get(api_path, params=pagination.dict())

    mock_get_assets.assert_called_once_with(
        asset_type=asset_type, pagination=pagination
    )
    assert res.status_code == 200
    assets = res.json()
    assert isinstance(assets, list) and len(assets) == 1
    asset_obj = asset_class(**assets[0])
    assert asset_obj.name == "asset_name" and asset_obj.identifier == 42


@pytest.mark.parametrize(
    "api_path, asset_type, asset_class",
    [
        ("/v1/assets/datasets/my", AssetType.DATASETS, Dataset),
        ("/v1/assets/models/my", AssetType.ML_MODELS, MLModel),
    ],
)
@pytest.mark.asyncio
async def test_api_get_my_assets(client, mocker, api_path, asset_type, asset_class):
    mock_get_my_assets = mocker.patch(
        "app.routers.aiod.get_my_assets",
        return_value=[{"name": "asset_name", "identifier": 42}],
    )

    res = client.get(api_path, headers={"Authorization": "valid-user-token"})

    mock_get_my_assets.assert_called_once_with(
        asset_type=asset_type, token="valid-user-token"
    )
    assert res.status_code == 200
    assets = res.json()
    assert isinstance(assets, list) and len(assets) == 1
    asset_obj = asset_class(**assets[0])
    assert asset_obj.name == "asset_name" and asset_obj.identifier == 42


@pytest.mark.parametrize(
    "api_path, asset_type, asset_class",
    [
        ("/v1/assets/datasets/search/asset_name", AssetType.DATASETS, Dataset),
        ("/v1/assets/models/search/asset_name", AssetType.ML_MODELS, MLModel),
        (
            "/v1/assets/publications/search/asset_name",
            AssetType.PUBLICATIONS,
            Publication,
        ),
    ],
)
@pytest.mark.asyncio
async def test_api_search_assets(client, mocker, api_path, asset_type, asset_class):
    pagination = Pagination(offset=7, limit=13)
    mock_search_assets = mocker.patch(
        "app.routers.aiod.search_assets",
        return_value=[{"name": "asset_name", "identifier": 42}],
    )

    res = client.get(api_path, params=pagination.dict())

    mock_search_assets.assert_called_once_with(
        asset_type=asset_type, query="asset_name", pagination=pagination
    )
    assert res.status_code == 200
    assets = res.json()
    assert isinstance(assets, list) and len(assets) == 1
    asset_obj = asset_class(**assets[0])
    assert asset_obj.name == "asset_name" and asset_obj.identifier == 42


@pytest.mark.parametrize(
    "api_path, asset_type, asset_class",
    [
        ("/v1/assets/datasets/42", AssetType.DATASETS, Dataset),
        ("/v1/assets/models/42", AssetType.ML_MODELS, MLModel),
        ("/v1/assets/publications/42", AssetType.PUBLICATIONS, Publication),
    ],
)
@pytest.mark.asyncio
async def test_api_get_asset(client, mocker, api_path, asset_type, asset_class):
    mock_get_asset = mocker.patch(
        "app.routers.aiod.get_asset",
        return_value={"name": "asset_name", "identifier": 42},
    )

    res = client.get(api_path)

    mock_get_asset.assert_called_once_with(asset_type=asset_type, asset_id=42)
    assert res.status_code == 200
    asset_obj = asset_class(**res.json())
    assert asset_obj.name == "asset_name" and asset_obj.identifier == 42


@pytest.mark.parametrize(
    "api_path, asset_type",
    [
        ("/v1/assets/counts/datasets", AssetType.DATASETS),
        ("/v1/assets/counts/models", AssetType.ML_MODELS),
        ("/v1/assets/counts/publications", AssetType.PUBLICATIONS),
    ],
)
@pytest.mark.asyncio
async def test_api_get_assets_count(client, mocker, api_path, asset_type):
    mock_get_assets_count = mocker.patch(
        "app.routers.aiod.get_assets_count",
        return_value=7,
    )

    res = client.get(api_path)

    mock_get_assets_count.assert_called_once_with(asset_type=asset_type)
    assert res.status_code == 200
    assert isinstance(res.json(), int) and res.json() == 7


@pytest.mark.parametrize(
    "api_path, asset_type",
    [
        ("/v1/assets/counts/datasets/search/asset_name", AssetType.DATASETS),
        ("/v1/assets/counts/models/search/asset_name", AssetType.ML_MODELS),
        ("/v1/assets/counts/publications/search/asset_name", AssetType.PUBLICATIONS),
    ],
)
@pytest.mark.asyncio
async def test_api_get_filtered_assets_count(client, mocker, api_path, asset_type):
    mock_get_assets_count = mocker.patch(
        "app.routers.aiod.get_assets_count",
        return_value=7,
    )

    res = client.get(api_path)

    mock_get_assets_count.assert_called_once_with(
        asset_type=asset_type, filter_query="asset_name"
    )
    assert res.status_code == 200
    assert isinstance(res.json(), int) and res.json() == 7
