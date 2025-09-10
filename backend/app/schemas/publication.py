from app.schemas.aiod_generated import PublicationRead
from app.schemas.asset_id import AssetId


class Publication(PublicationRead):
    identifier: AssetId
