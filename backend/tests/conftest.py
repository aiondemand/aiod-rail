from unittest.mock import AsyncMock

import pytest
from beanie import init_beanie
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient

from app.main import app
from app.models.rail_user import RailUser
from app.services.aiod import AsyncClientWrapper, aiod_client_wrapper


@pytest.fixture(scope="module")
def client():
    aiod_client_wrapper.start()
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
async def db_init():
    await init_beanie(
        database=AsyncMongoMockClient()["tests"],
        document_models=[RailUser],
    )


@pytest.fixture
def async_client_mock(mocker):
    return mocker.patch.object(AsyncClientWrapper, "client", new_callable=AsyncMock)
