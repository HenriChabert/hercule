from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.schemas.webhook import WebhookCreate
from tests.helpers.fakers.webhook import get_fake_webhook
from src.app.crud.webhook import WebhookCRUD
import pytest

@pytest.mark.asyncio
async def test_create_webhook(db: AsyncSession):
    fake_webhook = get_fake_webhook()
    webhook_crud = WebhookCRUD(db)
    created_webhook = await webhook_crud.create(WebhookCreate(
        name=fake_webhook.name,
        url=fake_webhook.url
    ))
    assert created_webhook.url == fake_webhook.url
    assert created_webhook.name == fake_webhook.name