from app.schemas.aiod_generated import PlatformRead  # type: ignore[attr-defined]
from app.schemas.asset_id import AssetId


class Platform(PlatformRead):
    identifier: AssetId
