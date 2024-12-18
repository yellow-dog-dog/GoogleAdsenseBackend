from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello World'}

def test_device():
    response = client.get("/api/device/all")
    assert response.status_code == 200
