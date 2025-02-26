from fixtures.api_client import *  # noqa: F403, F401
from fastapi.testclient import TestClient

from app import config


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


def test_get_fibonacci_list_pagination(client: TestClient):
    """ Requesting a list of fibonacci numbers. """
    response = client.get("/fibonacci/?page=1&limit=5")
    assert response.status_code == 200
    assert response.json() == {
        "page": 1,
        "limit": 5,
        "fibonacci_numbers": [
            {"index": 0, "number": 0},
            {"index": 1, "number": 1},
            {"index": 2, "number": 1},
            {"index": 3, "number": 2},
            {"index": 4, "number": 3}
        ]
    }

    response = client.get("/fibonacci/?page=2&limit=5")
    assert response.status_code == 200
    assert response.json() == {
        "page": 2,
        "limit": 5,
        "fibonacci_numbers": [
            {"index": 5, "number": 5},
            {"index": 6, "number": 8},
            {"index": 7, "number": 13},
            {"index": 8, "number": 21},
            {"index": 9, "number": 34},
        ]
    }


def test_invalid_pagination_requested(client: TestClient):
    """ Requesting a page that does not exists returns 404. """

    response = client.get("/fibonacci/?page=1002&limit=100")
    assert response.status_code == 422


def test_large_page_requested(client: TestClient):
    """ Requesting a larger page than allowed. """

    response = client.get("/fibonacci/?limit=1001")
    assert response.status_code == 422


def test_negative_or_zero_page_or_limit(client: TestClient):
    """ Requesting invalid pages"""

    response = client.get("/fibonacci/?limit=-1")
    assert response.status_code == 422

    response = client.get("/fibonacci/?limit=0")
    assert response.status_code == 422

    response = client.get("/fibonacci/?page=-1")
    assert response.status_code == 422

    response = client.get("/fibonacci/?page=0")
    assert response.status_code == 422


def test_large_page_for_large_numbers(client: TestClient):
    """ Requesting a large page for large numbers. """

    response = client.get("/fibonacci/?page=100&limit=1000")
    assert response.status_code == 422


def test_last_page_has_less_items(client: TestClient):
    """ Requesting the last page has less items. """
    max_page = config.max_number // 100 + 1
    response = client.get(f"/fibonacci/?page={max_page}&limit=100")
    assert response.status_code == 200
    assert len(response.json()["fibonacci_numbers"]) == 1
