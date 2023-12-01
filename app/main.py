import asyncio

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from app import __version__
from app.config import settings
from app.helpers import aiod_client_wrapper
from app.models.experiment import Experiment
from app.models.experiment_run import ExperimentRun
from app.models.experiment_template import ExperimentTemplate
from app.routers import aiod, experiment_templates, experiments
from app.services.experiment import ExperimentService

app = FastAPI(title="AIOD - Practitioner's Portal", version=__version__)

app.include_router(aiod.router, prefix="/v1/assets", tags=["assets"])
app.include_router(
    experiment_templates.router, prefix="/v1", tags=["experiment-templates"]
)
app.include_router(experiments.router, prefix="/v1", tags=["experiments"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
        document_models=[ExperimentTemplate, Experiment, ExperimentRun],
    )

    # Setup DockerClient and create queue of ExperimentRuns to execute
    docker_service = await ExperimentService.init_docker_service()

    # Create task for scheduling docker image builds for ExperimentTemplates from queue
    asyncio.create_task(docker_service.schedule_image_building())

    # Create task for scheduling ExperimentRuns from queue
    asyncio.create_task(docker_service.schedule_experiment_runs())


@app.on_event("shutdown")
async def shutdown_event():
    if getattr(app, "db", None) is not None:
        app.db.client.close()

    ExperimentService.get_docker_service().close_docker_connection()

    await aiod_client_wrapper.stop()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000, host="0.0.0.0")
