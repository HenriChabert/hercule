import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from sqlalchemy.orm.session import Session
from src.app.models.trigger import Trigger
from tests.helpers.fakers.trigger import TriggerFaker
from tests.helpers.fakers.webhook import WebhookFaker

from src.app.models import Webhook, Trigger

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

    trigger = db_sync.query(Trigger).filter(Trigger.id == data["id"]).first()
    assert trigger is not None
    assert trigger.name == trigger.name
    assert trigger.webhook_id == webhook.id

def test_create_trigger_with_webhook_url(db_sync: Session, client: TestClient):
    trigger = trigger_faker.get_fake()
    response = client.post("/api/v1/trigger", json={
        "name": trigger.name,
        "webhook_url": "https://example.com",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == trigger.name

    webhook = db_sync.query(Webhook).filter(Webhook.url == "https://example.com").first()
    assert webhook is not None
    assert data["webhook_id"] == webhook.id

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

def test_list_triggers_with_event(db_sync: Session, client: TestClient):
    # Create two triggers
    _ = trigger_faker.create_fake(db_sync, {
        "event": "page_opened"
    })
    _ = trigger_faker.create_fake(db_sync, {
        "event": "button_clicked"
    })
    
    response = client.get("/api/v1/triggers?event=page_opened")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["event"] == "page_opened"

def test_list_triggers_no_key(client_no_key: TestClient):
    response = client_no_key.get("/api/v1/triggers")
    assert response.status_code == 403

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

def test_run_trigger_success(db_sync: Session, client: TestClient, test_api_url: str):

    webhook = webhook_faker.create_fake(db_sync, {
        "url": f"{test_api_url}/test_webhook",
    })

    trigger = trigger_faker.create_fake(db_sync, {
        "webhook_id": webhook.id,
    })

    payload = {"test": "payload"}

    response = client.post(f"/api/v1/trigger/{trigger.id}/run", json={
        "payload": payload
    })

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

def test_trigger_event_success(db_sync: Session, client: TestClient, test_api_url: str):
    webhook = webhook_faker.create_fake(db_sync, {
        "url": f"{test_api_url}/test_webhook",
    })

    _ = trigger_faker.create_fake(db_sync, {
        "webhook_id": webhook.id,
        "event": "page_opened"
    })

    payload = {"url": "https://example.com"}

    response = client.post(f"/api/v1/triggers/event", json={
        "event": "page_opened",
        "context": payload
    })

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

def test_trigger_event_show_console_action(db_sync: Session, client: TestClient, test_api_url: str):
    webhook = webhook_faker.create_fake(db_sync, {
        "url": f"{test_api_url}/test_show_console_action",
    })

    _ = trigger_faker.create_fake(db_sync, {
        "webhook_id": webhook.id,
        "event": "page_opened"
    })

    payload = {"url": "https://example.com"}

    response = client.post(f"/api/v1/triggers/event", json={
        "event": "page_opened",
        "context": payload
    })

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    assert data[0]["actions"][0]["type"] == "show_console"
    assert data[0]["actions"][0]["params"]["message"] == "Test Works"
