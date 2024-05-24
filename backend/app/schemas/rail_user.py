from pydantic import BaseModel


class RailUser(BaseModel):
    email: str
    api_key: str = ""


class RailUserCreate(RailUser):
    pass


class RailUserResponse(RailUser):
    pass
