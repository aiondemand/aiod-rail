import pytest
from fastapi.testclient import TestClient

from app.helpers import aiod_client_wrapper
from app.main import app


@pytest.fixture(scope="session")
def client():
    aiod_client_wrapper.start()
    return TestClient(app)
