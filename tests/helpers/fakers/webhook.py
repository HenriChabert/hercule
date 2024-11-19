import datetime

import uuid as uuid_pkg
from sqlalchemy.ext.asyncio import AsyncSession
from typing import cast, TypedDict, NotRequired

from src.app import models
from tests.conftest import fake

class WebhookDict(TypedDict):
    id: NotRequired[uuid_pkg.UUID]
    name: NotRequired[str]
    auth_token: NotRequired[str]
    url: NotRequired[str]
    created_at: NotRequired[datetime.datetime]
    updated_at: NotRequired[datetime.datetime]

def get_fake_webhook(fields: WebhookDict | None = None) -> models.Webhook:
    if fields is None:
        fields = WebhookDict()

    return models.Webhook(
        id=fields.get("id", cast(uuid_pkg.UUID, fake.uuid4())),
        name=fields.get("name", fake.name()),
        auth_token=fields.get("auth_token", cast(str, fake.uuid4())),
        url=fields.get("url", fake.url()),
        created_at=fields.get("created_at", datetime.datetime.now()),
        updated_at=fields.get("updated_at", datetime.datetime.now()),
    )

async def create_fake_webhook(db: AsyncSession, fields: WebhookDict | None = None) -> models.Webhook:
    webhook = get_fake_webhook(fields)
    db.add(webhook)
    await db.commit()
    await db.refresh(webhook)
    return webhook
