from pydantic import BaseModel


class User(BaseModel):
    email: str
    api_key: str = ""


class UserCreate(User):
    pass


class UserResponse(User):
    pass
