from fastapi.testclient import TestClient

from app.main import app


def test_root_health_endpoint_returns_running_status() -> None:
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "running"}


def test_health_endpoint_returns_healthy_status() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
