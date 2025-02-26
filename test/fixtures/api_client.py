from app import api
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    app = api.create()
    return TestClient(app)
