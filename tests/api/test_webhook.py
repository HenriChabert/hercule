import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from sqlalchemy.orm.session import Session
from src.app.models.webhook import Webhook
from tests.helpers.fakers.webhook import WebhookFaker

webhook_faker = WebhookFaker()

def test_create_webhook_success(client: TestClient):
    fake_webhook = webhook_faker.get_fake()
    response = client.post("/api/v1/webhook", json={
        "name": fake_webhook.name,
        "url": fake_webhook.url,
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == fake_webhook.name
    assert data["url"] == fake_webhook.url
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_create_webhook_invalid_url(client: TestClient):
    webhook_data = {
        "name": "Test Webhook",
        "url": "not_a_url",
        "auth_token": "test_token"
    }
    response = client.post("/api/v1/webhook", json=webhook_data)
    assert response.status_code == 422

def test_get_webhook_success(db_sync: Session, client: TestClient):
    # First create a webhook
    webhook = webhook_faker.create_fake(db_sync)
    
    # Then get it
    response = client.get(f"/api/v1/webhook/{webhook.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == webhook.name
    assert data["url"] == webhook.url

def test_get_webhook_not_found(client: TestClient):
    response = client.get(f"/api/v1/webhook/{uuid4()}")
    assert response.status_code == 404

def test_list_webhooks(db_sync: Session, client: TestClient):
    # Create two webhooks
    _ = webhook_faker.create_fake(db_sync)
    _ = webhook_faker.create_fake(db_sync)
    
    response = client.get("/api/v1/webhooks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert isinstance(data, list)

def test_list_webhooks_no_key(client_no_key: TestClient):
    response = client_no_key.get("/api/v1/webhooks")
    assert response.status_code == 403

def test_update_webhook_success(db_sync: Session, client: TestClient):
    # First create a webhook
    webhook = webhook_faker.create_fake(db_sync)
    webhook_id = webhook.id
    
    # Then update it
    new_fake_webhook = webhook_faker.get_fake()
    response = client.put(f"/api/v1/webhook/{webhook_id}", json={
        "name": new_fake_webhook.name,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_fake_webhook.name
    assert data["url"] == webhook.url

def test_update_webhook_not_found(client: TestClient):
    new_fake_webhook = webhook_faker.get_fake()
    response = client.put(f"/api/v1/webhook/{uuid4()}", json={
        "name": new_fake_webhook.name,
    })
    assert response.status_code == 404

def test_delete_webhook_success(db_sync: Session, client: TestClient):
    # First create a webhook
    fake_webhook = webhook_faker.create_fake(db_sync)
    
    # Then delete it
    response = client.delete(f"/api/v1/webhook/{fake_webhook.id}")
    assert response.status_code == 200
    
    # Verify it's gone
    webhooks = db_sync.query(Webhook).all()
    assert len(webhooks) == 0

def test_delete_webhook_not_found(client: TestClient):
    response = client.delete(f"/api/v1/webhook/{uuid4()}")
    assert response.status_code == 404