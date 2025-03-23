from fastapi.testclient import TestClient


def test_health(client_anon: TestClient):
    response = client_anon.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_secured(client_auth: TestClient):
    response = client_auth.get("/api/v1/health-secured")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_secured_unauthenticated(client_anon: TestClient):
    response = client_anon.get("/api/v1/health-secured")
    assert response.status_code == 401
