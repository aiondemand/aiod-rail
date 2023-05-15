from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from app import __version__
from app.config import settings
from app.models.experiment import Experiment
from app.routers import experiments, metadata
from app.routers.metadata import aiod_client_wrapper

app = FastAPI(title="AIOD - Practitioner's Portal", version=__version__)

app.include_router(metadata.router, prefix="/v1", tags=["metadata"])
app.include_router(experiments.router, prefix="/v1", tags=["experiments"])


@app.on_event("startup")
async def app_init():
    """Initialize application services"""
    aiod_client_wrapper.start()

    app.db = AsyncIOMotorClient(settings.MONGODB_URI, uuidRepresentation="standard")[
        settings.MONGODB_DBNAME
    ]

    await init_beanie(
        database=app.db,
        document_models=[Experiment],
    )


@app.on_event("shutdown")
async def shutdown_event():
    await aiod_client_wrapper.stop()
