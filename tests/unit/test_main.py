"""Test for main.py."""
from fastapi.testclient import TestClient

from api.main import app

test_client = TestClient(app)


def test_root():
    """Unit test for root get API call."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI Course!"}
