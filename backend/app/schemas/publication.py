from app.schemas.aiod_generated import PublicationRead  # type: ignore[attr-defined]
from app.schemas.asset_id import AssetId


class Publication(PublicationRead):
    identifier: AssetId
