import httpx
from fastapi import APIRouter

from app.config import settings

router = APIRouter()


class AIoDClientWrapper:
    async_client = None

    def start(self):
        """Instantiate the client. Call from the FastAPI startup hook."""
        self.async_client = httpx.AsyncClient()

    async def stop(self):
        """Gracefully shutdown. Call from FastAPI shutdown hook."""
        await self.async_client.aclose()
        self.async_client = None

    def __call__(self):
        """Calling the instantiated HTTPXClientWrapper returns the wrapped singleton."""
        assert self.async_client is not None
        return self.async_client


aiod_client_wrapper = AIoDClientWrapper()


@router.get("/datasets")
async def get_datasets(offset: int = 0, limit: int = 100):
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        f"{settings.METADATA_API_BASE_URL}/datasets/v0",
        params={"offset": offset, "limit": limit},
    )
    return res.json()


@router.get("/publications")
async def get_publications(offset: int = 0, limit: int = 100):
    async_client = aiod_client_wrapper()
    res = await async_client.get(
        f"{settings.METADATA_API_BASE_URL}/publications/v0",
        params={"offset": offset, "limit": limit},
    )
    return res.json()
