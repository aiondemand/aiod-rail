import secrets

from beanie import Document

from app.schemas.rail_user import RailUserResponse


class RailUser(Document):
    email: str
    api_key: str = ""

    class Settings:
        name = "rail_users"

    @classmethod
    def generate_api_key(cls) -> str:
        return secrets.token_hex(16)

    def to_dict(self) -> dict:
        return {"email": self.email, "api_key": self.api_key}

    def map_to_response(self) -> RailUserResponse:
        return RailUserResponse(email=self.email, api_key=self.api_key)
