from app.schemas.aiod_generated import PlatformRead
from app.schemas.asset_id import AssetId


class Platform(PlatformRead):
    identifier: AssetId
