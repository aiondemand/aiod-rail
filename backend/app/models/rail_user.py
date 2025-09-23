from beanie import Document

from app.schemas.rail_user import RailUserResponse


class RailUser(Document):
    email: str
    api_key: str = ""

    class Settings:
        name = "rail_users"

    def to_dict(self) -> dict:
        return {"email": self.email, "api_key": self.api_key}

    def map_to_response(self) -> RailUserResponse:
        return RailUserResponse(**self.to_dict())
