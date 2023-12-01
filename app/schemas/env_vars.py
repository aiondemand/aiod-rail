from pydantic import BaseModel


class EnvironmentVarDef(BaseModel):
    name: str
    description: str


class EnvironmentVar(BaseModel):
    key: str
    value: str
