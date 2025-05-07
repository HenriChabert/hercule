from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import Session

from src.app.models import Trigger, Webhook, WebhookUsage
from src.app.models.trigger import Trigger
from tests.helpers.fakers.trigger import TriggerFaker
from tests.helpers.fakers.webhook import WebhookFaker

trigger_faker = TriggerFaker()
webhook_faker = WebhookFaker()


@pytest.mark.asyncio
async def test_create_trigger_success(client_admin: TestClient, db: AsyncSession):
    trigger = trigger_faker.get_fake()
    webhook = await webhook_faker.create_fake(db)

    response = client_admin.post(
        "/api/v1/trigger",
        json={
            "name": trigger.name,
            "webhook_id": webhook.id,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == trigger.name
    assert data["webhook_id"] == webhook.id

    trigger_result = await db.execute(select(Trigger).where(Trigger.id == data["id"]))
    trigger = trigger_result.scalar_one_or_none()
    assert trigger is not None
    assert trigger.name == trigger.name
    assert trigger.webhook_id == webhook.id


@pytest.mark.asyncio
async def test_create_trigger_with_manual_trigger_in_popup(
    db: AsyncSession, client_admin: TestClient
):
    trigger = trigger_faker.get_fake()
    webhook = await webhook_faker.create_fake(db)

    response = client_admin.post(
        "/api/v1/trigger",
        json={
            "name": trigger.name,
            "event": "manual_trigger_in_popup",
            "webhook_id": webhook.id,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == trigger.name
    assert data["webhook_id"] == webhook.id


@pytest.mark.asyncio
async def test_create_trigger_unauthorized(client_auth: TestClient):
    trigger = trigger_faker.get_fake()
    response = client_auth.post(
        "/api/v1/trigger",
        json={"name": trigger.name, "webhook_id": "123"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_trigger_unauthenticated(client_anon: TestClient):
    trigger = trigger_faker.get_fake()
    response = client_anon.post(
        "/api/v1/trigger",
        json={"name": trigger.name, "webhook_id": "123"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_trigger_with_webhook_url(
    db: AsyncSession, client_admin: TestClient
):
    trigger = trigger_faker.get_fake()
    response = client_admin.post(
        "/api/v1/trigger",
        json={
            "name": trigger.name,
            "webhook_url": "https://example.com",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == trigger.name

    webhook = await db.execute(
        select(Webhook).where(Webhook.url == "https://example.com")
    )
    webhook = webhook.scalar_one_or_none()
    assert webhook is not None
    assert data["webhook_id"] == webhook.id


@pytest.mark.asyncio
async def test_create_trigger_invalid_webhook(client_admin: TestClient):
    fake_trigger = trigger_faker.get_fake()
    response = client_admin.post(
        "/api/v1/trigger",
        json={
            "name": fake_trigger.name,
            "webhook_id": str(uuid4()),
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_trigger_success(db: AsyncSession, client_auth: TestClient):
    # First create a trigger
    trigger = await trigger_faker.create_fake(db)

    # Then get it
    response = client_auth.get(f"/api/v1/trigger/{trigger.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == trigger.name
    assert data["webhook_id"] == trigger.webhook_id


def test_get_trigger_not_found(client_auth: TestClient):
    response = client_auth.get(f"/api/v1/trigger/{uuid4()}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_triggers(db: AsyncSession, client_auth: TestClient):
    # Create two triggers
    _ = await trigger_faker.create_fake(db)
    _ = await trigger_faker.create_fake(db)

    response = client_auth.get("/api/v1/triggers")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_list_triggers_with_event(db: AsyncSession, client_auth: TestClient):
    # Create two triggers
    _ = await trigger_faker.create_fake(db, {"event": "page_opened"})
    _ = await trigger_faker.create_fake(db, {"event": "button_clicked"})

    response = client_auth.get("/api/v1/triggers?event=page_opened")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["event"] == "page_opened"


@pytest.mark.asyncio
async def test_update_trigger_success(db: AsyncSession, client_admin: TestClient):
    # First create a trigger
    trigger = await trigger_faker.create_fake(db)
    trigger_id = trigger.id

    # Then update it
    new_trigger = trigger_faker.get_fake()
    response = client_admin.put(
        f"/api/v1/trigger/{trigger_id}",
        json={
            "name": new_trigger.name,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_trigger.name
    assert data["webhook_id"] == trigger.webhook_id


def test_update_trigger_not_found(client_admin: TestClient):
    new_trigger = trigger_faker.get_fake()
    response = client_admin.put(
        f"/api/v1/trigger/{uuid4()}",
        json={
            "name": new_trigger.name,
        },
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_trigger_success(db: AsyncSession, client_admin: TestClient):
    # First create a trigger
    trigger = await trigger_faker.create_fake(db)

    # Then delete it
    response = client_admin.delete(f"/api/v1/trigger/{trigger.id}")
    assert response.status_code == 200

    # Verify it's gone
    triggers = await db.execute(select(Trigger))
    triggers = triggers.scalars().all()
    assert len(triggers) == 0


@pytest.mark.asyncio
async def test_delete_trigger_not_found(client_admin: TestClient):
    response = client_admin.delete(f"/api/v1/trigger/{uuid4()}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_run_trigger_success(
    db: AsyncSession, client_auth: TestClient, test_api_url: str
):

    webhook = await webhook_faker.create_fake(
        db,
        {
            "url": f"{test_api_url}/test_webhook",
        },
    )

    trigger = await trigger_faker.create_fake(
        db,
        {
            "webhook_id": webhook.id,
        },
    )

    context = {"url": "https://example.com"}

    response = client_auth.post(
        f"/api/v1/trigger/{trigger.id}/run",
        json={"event": trigger.event, "context": context},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


@pytest.mark.asyncio
async def test_trigger_event_success(
    db: AsyncSession, client_auth: TestClient, test_api_url: str
):
    webhook = await webhook_faker.create_fake(
        db,
        {
            "url": f"{test_api_url}/test_webhook",
        },
    )

    _ = await trigger_faker.create_fake(
        db, {"webhook_id": webhook.id, "event": "page_opened"}
    )

    payload = {"url": "https://example.com"}

    response = client_auth.post(
        f"/api/v1/triggers/event", json={"event": "page_opened", "context": payload}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    webhook_usage = await db.execute(
        select(WebhookUsage).where(WebhookUsage.webhook_id == webhook.id)
    )
    webhook_usage = webhook_usage.scalar_one_or_none()

    assert webhook_usage is not None
    assert webhook_usage.status == "success"


@pytest.mark.asyncio
async def test_trigger_event_error(
    db: AsyncSession, client_auth: TestClient, test_api_url: str
):
    webhook = await webhook_faker.create_fake(
        db,
        {
            "url": f"{test_api_url}/test_webhook_error",
        },
    )

    _ = await trigger_faker.create_fake(
        db, {"webhook_id": webhook.id, "event": "page_opened"}
    )

    payload = {"url": "https://example.com"}

    response = client_auth.post(
        f"/api/v1/triggers/event", json={"event": "page_opened", "context": payload}
    )

    assert response.status_code == 400
    data = response.json()
    details = data["detail"]

    assert details["status"] == 500
    assert details["message"] == '{"detail":"Test Error"}'

    webhook_usage = await db.execute(
        select(WebhookUsage).where(WebhookUsage.webhook_id == webhook.id)
    )
    webhook_usage = webhook_usage.scalar_one_or_none()

    assert webhook_usage is not None
    assert webhook_usage.status == "error"


@pytest.mark.asyncio
async def test_trigger_event_show_console_action(
    db: AsyncSession, client_auth: TestClient, test_api_url: str
):
    webhook = await webhook_faker.create_fake(
        db,
        {
            "url": f"{test_api_url}/test_show_console_action",
        },
    )

    _ = await trigger_faker.create_fake(
        db, {"webhook_id": webhook.id, "event": "page_opened"}
    )

    payload = {"url": "https://example.com"}

    response = client_auth.post(
        f"/api/v1/triggers/event", json={"event": "page_opened", "context": payload}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    assert data[0]["actions"][0]["type"] == "show_console"
    assert data[0]["actions"][0]["params"]["message"] == "Test Works"
