from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.aiod import AIoDClientWrapper, aiod_client_wrapper


@pytest.fixture(scope="module")
def client():
    aiod_client_wrapper.start()
    return TestClient(app)


@pytest.fixture
def aiod_client_mock(mocker):
    return mocker.patch.object(AIoDClientWrapper, "client", new_callable=AsyncMock)
