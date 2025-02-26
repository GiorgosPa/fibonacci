from fixtures.api_client import *  # noqa: F403, F401
from fastapi.testclient import TestClient


def test_request_blacklisted_number(client: TestClient):
    """ Requesting a blacklisted number returns 403. """
    client.post('/blacklist/5')
    response = client.get('/fibonacci/5')
    assert response.status_code == 403
    assert response.json() == {"detail": "Number 5 is blacklisted."}


def test_request_a_list_with_blacklisted_number(client: TestClient):
    """ Requesting a list of fibonacci numbers with a blacklisted number omits the blacklisted number. """
    client.post('/blacklist/5')
    response = client.get('/fibonacci/?page=1&limit=7')
    assert response.status_code == 200
    assert response.json() == {
        "page": 1,
        "limit": 7,
        "fibonacci_numbers": [
            {"index": 0, "number": 0},
            {"index": 1, "number": 1},
            {"index": 2, "number": 1},
            {"index": 3, "number": 2},
            {"index": 4, "number": 3},
            {"index": 6, "number": 8},
        ]
    }
