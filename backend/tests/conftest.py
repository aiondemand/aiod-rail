import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.aiod import aiod_client_wrapper


@pytest.fixture(scope="session")
def client():
    aiod_client_wrapper.start()
    return TestClient(app)
