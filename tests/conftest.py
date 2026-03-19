import pytest
from fastapi.testclient import TestClient

from app.api.v1.dependencies import connection_manager, job_storage
from app.main import app


@pytest.fixture(autouse=True)
def clear_storage():
    job_storage._storage.clear()
    connection_manager._subscriptions.clear()
    yield


@pytest.fixture
def client():
    return TestClient(app)
