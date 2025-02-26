from app import api
from app.fibonacci import model
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    app = api.create()
    model.compute_fibonacci_number()
    return TestClient(app)
