from typing import Generic, Mapping, Optional, TypeVar
from pydantic import BaseModel, Field, StrictBytes, StrictInt

T = TypeVar("T")

"""
    Model for API responses.
"""


class ApiResponse(BaseModel, Generic[T]):

    status_code: StrictInt = Field(description="HTTP status code")
    headers: Optional[Mapping[str, str]] = Field(None, description="HTTP headers")
    data: T = Field(description="Deserialized data given the data type")
    raw_data: StrictBytes = Field(description="Raw data (HTTP response body)")

    model_config = {"arbitrary_types_allowed": True}
