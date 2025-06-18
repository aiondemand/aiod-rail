from typing import Annotated

from pydantic import Field

str = Annotated[str, Field(description="AIoD assset ID", max_length=50)]
