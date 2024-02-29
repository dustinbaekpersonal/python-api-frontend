"""Test for main.py."""
# from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.main import app

# app = FastAPI()

# @app.get("/")
# async def read_main():
#     return {"msg": "Hello World"}

test_client = TestClient(app)


def test_root():
    """Unit test for root get API call."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
