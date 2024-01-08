from enum import Enum

import httpx
from pydantic import BaseModel

from app.config import settings


class Pagination(BaseModel):
    offset: int = 0
    limit: int = settings.DEFAULT_RESPONSE_LIMIT


class QueryOperator(str, Enum):
    OR = "OR"
    AND = "AND"


class AIoDClientWrapper:
    async_client = None

    def start(self):
        """Instantiate the client. Call from the FastAPI startup hook."""
        self.async_client = httpx.AsyncClient(verify=settings.AIOD_API.VERIFY_SSL)

    async def stop(self):
        """Gracefully shutdown. Call from FastAPI shutdown hook."""
        await self.async_client.aclose()
        self.async_client = None

    def __call__(self):
        """Calling the instantiated HTTPXClientWrapper returns the wrapped singleton."""
        assert self.async_client is not None
        return self.async_client


aiod_client_wrapper = AIoDClientWrapper()
