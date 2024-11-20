import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from sqlalchemy.orm.session import Session
from src.app.models.trigger import Trigger
from tests.helpers.fakers.trigger import TriggerFaker
from tests.helpers.fakers.webhook import WebhookFaker

trigger_faker = TriggerFaker()
webhook_faker = WebhookFaker()

def test_create_trigger_success(db_sync: Session, client: TestClient):
    trigger = trigger_faker.get_fake()
    webhook = webhook_faker.create_fake(db_sync)
    response = client.post("/api/v1/trigger", json={
        "name": trigger.name,
        "webhook_id": webhook.id,
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == trigger.name
    assert data["webhook_id"] == webhook.id
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_create_trigger_invalid_webhook(client: TestClient):
    fake_trigger = trigger_faker.get_fake()
    response = client.post("/api/v1/trigger", json={
        "name": fake_trigger.name,
        "webhook_id": str(uuid4()),
    })
    assert response.status_code == 422

def test_get_trigger_success(db_sync: Session, client: TestClient):
    # First create a trigger
    trigger = trigger_faker.create_fake(db_sync)
    
    # Then get it
    response = client.get(f"/api/v1/trigger/{trigger.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == trigger.name
    assert data["webhook_id"] == trigger.webhook_id

def test_get_trigger_not_found(client: TestClient):
    response = client.get(f"/api/v1/trigger/{uuid4()}")
    assert response.status_code == 404

def test_list_triggers(db_sync: Session, client: TestClient):
    # Create two triggers
    _ = trigger_faker.create_fake(db_sync)
    _ = trigger_faker.create_fake(db_sync)
    
    response = client.get("/api/v1/triggers")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert isinstance(data, list)

def test_update_trigger_success(db_sync: Session, client: TestClient):
    # First create a trigger
    trigger = trigger_faker.create_fake(db_sync)
    trigger_id = trigger.id
    
    # Then update it
    new_trigger = trigger_faker.get_fake()
    response = client.put(f"/api/v1/trigger/{trigger_id}", json={
        "name": new_trigger.name,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_trigger.name
    assert data["webhook_id"] == trigger.webhook_id

def test_update_trigger_not_found(client: TestClient):
    new_trigger = trigger_faker.get_fake()
    response = client.put(f"/api/v1/trigger/{uuid4()}", json={
        "name": new_trigger.name,
    })
    assert response.status_code == 404

def test_delete_trigger_success(db_sync: Session, client: TestClient):
    # First create a trigger
    trigger = trigger_faker.create_fake(db_sync)
    
    # Then delete it
    response = client.delete(f"/api/v1/trigger/{trigger.id}")
    assert response.status_code == 200
    
    # Verify it's gone
    triggers = db_sync.query(Trigger).all()
    assert len(triggers) == 0

def test_delete_trigger_not_found(client: TestClient):
    response = client.delete(f"/api/v1/trigger/{uuid4()}")
    assert response.status_code == 404