from fixtures.api_client import *  # noqa: F403, F401
from fastapi.testclient import TestClient

from app.blacklist import model


def test_add_to_blacklist(client: TestClient):
    response = client.post('/blacklist/5')
    assert response.status_code == 200
    assert 5 in model.blacklisted_numbers


def test_remove_from_blacklist(client):
    client.post('/blacklist/5')
    response = client.delete('/blacklist/5')
    assert response.status_code == 200
    assert 5 not in model.blacklisted_numbers


def test_remove_nonexistent_item(client):
    response = client.delete('/blacklist/5')
    assert response.status_code == 404


def test_add_invalid_number(client):
    response = client.post('/blacklist/-5')
    assert response.status_code == 422

    response = client.post('/blacklist/100001')
    assert response.status_code == 422


def test_remove_invalid_number(client):
    response = client.delete('/blacklist/-5')
    assert response.status_code == 422

    response = client.delete('/blacklist/100001')
    assert response.status_code == 422
