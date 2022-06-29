from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/predict")
    assert response.status_code == 422


def test_api_access_error():
    response = client.get("/predict?temperature=80&humidity=-80")
    assert response.status_code == 400


def test_api_access_pass():
    response = client.get("/predict?temperature=29&humidity=80")
    assert response.status_code == 444