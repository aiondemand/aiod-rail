from app.schemas.aiod_generated import DatasetRead
from app.schemas.asset_id import AssetId


class Dataset(DatasetRead):
    identifier: AssetId
