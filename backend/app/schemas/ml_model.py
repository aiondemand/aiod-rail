from app.schemas.aiod_generated import MLModelRead  # type: ignore[attr-defined]
from app.schemas.asset_id import AssetId


class MLModel(MLModelRead):
    identifier: AssetId
