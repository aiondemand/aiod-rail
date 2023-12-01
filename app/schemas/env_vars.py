from pydantic import BaseModel, constr


class EnvironmentVarDef(BaseModel):
    name: constr(to_upper=True)
    description: str


class EnvironmentVarValue(BaseModel):
    name: constr(to_upper=True)
    value: str
