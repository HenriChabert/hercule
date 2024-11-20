from fastapi.testclient import TestClient

def test_health(client: TestClient):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_health_secured(client: TestClient):
    response = client.get("/api/v1/health-secured")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_health_secured_no_key(client_no_key: TestClient):
    response = client_no_key.get("/api/v1/health-secured")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}

def test_health_secured_invalid_key(client: TestClient):
    response = client.get("/api/v1/health-secured", headers={"X-Hercule-Secret-Key": "invalid"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid secret key"}