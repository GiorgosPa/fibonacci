import sys

from app import api, config, blacklist
from app.fibonacci import model
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    config.max_number = 10_000
    blacklist.blacklisted_numbers.clear()
    app = api.create()
    model.compute_fibonacci_number()
    sys.set_int_max_str_digits(50_000)
    return TestClient(app)
