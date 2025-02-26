from fixtures.api_client import *  # noqa: F403, F401
from fastapi.testclient import TestClient


def test_get_fibonacci_as_number(client: TestClient):
    """ Requesting the fibonacci number as a number returns 400 if the number is too large. """
    response = client.get("/fibonacci/5?return_type=number")
    assert response.status_code == 200
    assert response.json() == 5

    response = client.get("/fibonacci/10000?return_type=number")
    assert response.status_code == 400


def test_get_fibonacci_as_string(client: TestClient):
    """ A large number can be returned as a string. """
    response = client.get("/fibonacci/5?return_type=string")
    assert response.status_code == 200
    assert response.json() == "5"

    response = client.get("/fibonacci/10000?return_type=string")
    assert response.status_code == 200
    assert isinstance(response.json(), str)


def test_get_fibonacci_auto(client: TestClient):
    """ By default the return type is auto and it returns a number
        until the result is too large where it switches to a string. """
    response = client.get("/fibonacci/5")
    assert response.status_code == 200
    assert response.json() == 5

    response = client.get("/fibonacci/10000")
    assert response.status_code == 200
    assert isinstance(response.json(), str)


def test_invalid_number_requested(client: TestClient):
    """ By default the return type is auto and it returns a number
        until the result is too large where it switches to a string. """
    response = client.get("/fibonacci/-1")
    assert response.status_code == 422

    response = client.get("/fibonacci/100001")
    assert response.status_code == 422
