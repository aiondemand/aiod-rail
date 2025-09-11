from __future__ import annotations

from pydantic import BaseModel


class EnvironmentVarDef(BaseModel):
    name: str
    description: str
    is_secret: bool


class EnvironmentVarBase(BaseModel):
    key: str
    value: str


class EnvironmentVarCreate(EnvironmentVarBase):
    pass


class EnvironmentVar(EnvironmentVarBase):
    is_secret: bool

    @classmethod
    def create_variable(
        cls, env_var: EnvironmentVarCreate, var_defs: list[EnvironmentVarDef]
    ) -> EnvironmentVar:
        secret_names = [var.name for var in var_defs if var.is_secret]

        return EnvironmentVar(**env_var.dict(), is_secret=env_var.key in secret_names)

    def censor(self, is_mine: bool) -> None:
        if self.is_secret and is_mine is False:
            self.value = "*****"
