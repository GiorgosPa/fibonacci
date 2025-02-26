from fixtures.api_client import *  # noqa: F403, F401
from fastapi.testclient import TestClient


def test_fibonacci(client: TestClient):
    """ Test the Fibonacci endpoint. """

    response = client.get("/fibonacci")
    assert response.status_code == 200
