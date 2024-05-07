from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.aiod import AsyncClientWrapper, aiod_client_wrapper


@pytest.fixture(scope="module")
def client():
    aiod_client_wrapper.start()
    return TestClient(app)


@pytest.fixture
def async_client_mock(mocker):
    return mocker.patch.object(AsyncClientWrapper, "client", new_callable=AsyncMock)
