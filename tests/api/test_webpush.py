from fastapi.testclient import TestClient

from src.app.core.config import settings


def test_get_public_key(client: TestClient):
    response = client.get("/api/v1/webpush/public-key")
    assert response.status_code == 200
    
    assert response.json() == {
        "public_key": settings.APP_SERVER_KEY
    }
