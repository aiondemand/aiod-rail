from pydantic import BaseModel


class RailUser(BaseModel):
    email: str
    api_key: str = ""


class RailUserResponse(RailUser):
    pass
