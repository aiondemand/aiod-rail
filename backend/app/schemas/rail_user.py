from pydantic import BaseModel


class RailUser(BaseModel):
    email: str


class RailUserResponse(RailUser):
    pass
