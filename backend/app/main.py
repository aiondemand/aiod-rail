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
from app.services.container_platforms.base_platform import ContainerBasePlatform
from app.services.container_platforms.docker import DockerService
from app.services.scheduling import ExperimentScheduling
from app.services.workflow_engines.base_engine import WorkflowBaseEngine
from app.services.workflow_engines.reana import ReanaService

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

    # initialize container platform and worfklow engine
    container_platform: ContainerBasePlatform = await DockerService.init()
    workflow_engine: WorkflowBaseEngine = await ReanaService.init()

    # Setup ExperimentScheduling and create queues of experiments and images to execute
    experiment_scheduling = await ExperimentScheduling.init(
        container_platform, workflow_engine
    )

    # Create seperate tasks for scheduling experiments and images
    asyncio.create_task(experiment_scheduling.schedule_image_building())
    asyncio.create_task(experiment_scheduling.schedule_experiment_runs())


@app.on_event("shutdown")
async def shutdown_event():
    if getattr(app, "db", None) is not None:
        app.db.client.close()

    await ContainerBasePlatform.get_service().terminate()

    await aiod_client_wrapper.stop()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000, host="0.0.0.0")
