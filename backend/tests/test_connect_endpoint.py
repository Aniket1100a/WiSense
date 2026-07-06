from fastapi.testclient import TestClient

from app.main import app


def test_connect_endpoint_returns_connected() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/connect")

    assert response.status_code == 200
    assert response.json() == {"ok": True, "message": "connected"}
