from app.schemas.aiod_generated import MLModelRead
from app.schemas.asset_id import AssetId


class MLModel(MLModelRead):
    identifier: AssetId
