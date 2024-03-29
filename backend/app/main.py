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
from app.services.container_platforms.base import ContainerPlatformBase
from app.services.container_platforms.docker import DockerService
from app.services.experiment_scheduler import ExperimentScheduler
from app.services.workflow_engines.base import WorkflowEngineBase
from app.services.workflow_engines.reana import ReanaService

app = FastAPI(title="AIoD - RAIL", version=__version__)

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

    # initialize container platform and workflow engine
    container_platform: ContainerPlatformBase = await DockerService.init()
    workflow_engine: WorkflowEngineBase = await ReanaService.init()

    # Setup ExperimentScheduler and create queues of experiments and images to execute
    experiment_scheduler = await ExperimentScheduler.init(
        container_platform, workflow_engine
    )

    # Create separate tasks for scheduling experiments and images
    asyncio.create_task(experiment_scheduler.schedule_image_building())
    asyncio.create_task(experiment_scheduler.schedule_experiment_runs())


@app.on_event("shutdown")
async def shutdown_event():
    if getattr(app, "db", None) is not None:
        app.db.client.close()

    await ContainerPlatformBase.get_service().terminate()

    await aiod_client_wrapper.stop()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000, host="0.0.0.0")
