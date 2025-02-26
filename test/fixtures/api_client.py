import sys
from app import api
from app.fibonacci import model
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    app = api.create()
    model.compute_fibonacci_number()
    sys.set_int_max_str_digits(50_000)
    return TestClient(app)
