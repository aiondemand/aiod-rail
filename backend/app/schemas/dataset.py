from app.schemas.aiod_generated import DatasetRead  # type: ignore[attr-defined]
from app.schemas.asset_id import AssetId


class Dataset(DatasetRead):
    identifier: AssetId
