import secrets
from beanie import Document

from app.schemas.user import UserResponse


class User(Document):
    email: str
    api_key: str = ""
    
    class Settings:
        name = "users"
    
    @classmethod
    def generate_api_key(cls) -> str:
        return secrets.token_hex(16)
    
    
    def to_dict(self) -> dict:
        return {
            "email": self.email, 
            "api_key": self.api_key
        }
    
    
    def map_to_response(self) -> UserResponse:
        return UserResponse(
            email=self.email, 
            api_key=self.api_key
        )
