from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import Session

from src.app.models.webhook import Webhook
from tests.helpers.fakers.webhook import WebhookFaker

webhook_faker = WebhookFaker()

@pytest.mark.asyncio
async def test_create_webhook_success(db: AsyncSession, client_admin: TestClient):
    fake_webhook = webhook_faker.get_fake()
    response = client_admin.post("/api/v1/webhook", json={
        "name": fake_webhook.name,
        "url": fake_webhook.url,
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == fake_webhook.name
    assert data["url"] == fake_webhook.url


    webhook = await db.execute(select(Webhook).where(Webhook.id == data["id"]))
    webhook = webhook.scalar_one_or_none()
    assert webhook is not None
    assert webhook.name == fake_webhook.name
    assert webhook.url == fake_webhook.url

def test_create_webhook_invalid_url(client_admin: TestClient):
    webhook_data = {
        "name": "Test Webhook",
        "url": "not_a_url",
        "auth_token": "test_token"
    }
    response = client_admin.post("/api/v1/webhook", json=webhook_data)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_webhook_success(db: AsyncSession, client_auth: TestClient):
    # First create a webhook
    webhook = await webhook_faker.create_fake(db)
    
    # Then get it
    response = client_auth.get(f"/api/v1/webhook/{webhook.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == webhook.name
    assert data["url"] == webhook.url

def test_get_webhook_not_found(client_auth: TestClient):
    response = client_auth.get(f"/api/v1/webhook/{uuid4()}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_list_webhooks(db: AsyncSession, client_auth: TestClient):
    # Create two webhooks
    _ = await webhook_faker.create_fake(db)
    _ = await webhook_faker.create_fake(db)
    
    response = client_auth.get("/api/v1/webhooks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert isinstance(data, list)

def test_list_webhooks_unauthenticated(client_anon: TestClient):
    response = client_anon.get("/api/v1/webhooks")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_update_webhook_success(db: AsyncSession, client_admin: TestClient):
    # First create a webhook
    webhook = await webhook_faker.create_fake(db)
    webhook_id = webhook.id
    
    # Then update it
    new_fake_webhook = webhook_faker.get_fake(fields={"name": "test"})
    response = client_admin.put(f"/api/v1/webhook/{webhook_id}", json={
        "name": new_fake_webhook.name,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_fake_webhook.name
    assert data["url"] == webhook.url
    
    new_webhook = await db.execute(select(Webhook).where(Webhook.id == webhook_id))
    new_webhook = new_webhook.scalar_one_or_none()
    assert new_webhook is not None
    assert new_webhook.name == new_fake_webhook.name
    assert new_webhook.url == webhook.url

def test_update_webhook_not_found(client_admin: TestClient):
    new_fake_webhook = webhook_faker.get_fake()
    response = client_admin.put(f"/api/v1/webhook/{uuid4()}", json={
        "name": new_fake_webhook.name,
    })
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_webhook_success(db: AsyncSession, client_admin: TestClient):
    # First create a webhook
    fake_webhook = await webhook_faker.create_fake(db)
    
    # Then delete it
    response = client_admin.delete(f"/api/v1/webhook/{fake_webhook.id}")
    assert response.status_code == 200
    
    # Verify it's gone
    webhooks = await db.execute(select(Webhook))
    webhooks = webhooks.scalars().all()
    assert len(webhooks) == 0

def test_delete_webhook_not_found(client_admin: TestClient):
    response = client_admin.delete(f"/api/v1/webhook/{uuid4()}")
    assert response.status_code == 404