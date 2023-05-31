from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from app import __version__
from app.config import settings
from app.helpers import aiod_client_wrapper
from app.models.experiment import Experiment
from app.routers import aiod, experiments

app = FastAPI(title="AIOD - Practitioner's Portal", version=__version__)

app.include_router(aiod.router, prefix="/v1", tags=["metadata"])
app.include_router(experiments.router, prefix="/v1", tags=["experiments"])

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
