from beanie import Document

from app.schemas.rail_user import RailUserResponse


class RailUser(Document):
    email: str
    api_key: str = ""

    class Settings:
        name = "rail_users"

    def map_to_response(self) -> RailUserResponse:
        return RailUserResponse(email=self.email)
