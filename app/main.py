from fastapi import FastAPI

from app import __version__
from app.routers import metadata
from app.routers.metadata import aiod_client_wrapper

app = FastAPI(title="AIOD - Practitioner's Portal", version=__version__)

app.include_router(metadata.router, prefix="/v1", tags=["metadata"])


@app.on_event("startup")
async def app_init():
    """Initialize application services"""
    aiod_client_wrapper.start()


@app.on_event("shutdown")
async def shutdown_event():
    await aiod_client_wrapper.stop()
