import datetime

import uuid as uuid_pkg
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Callable, cast, TypedDict, NotRequired, TypeVar, Mapping

from src.app.core.db.database import Base
from src.app import models, schemas
from tests.conftest import fake

T = TypeVar("T", bound=Base)

class WebhookDict(TypedDict):
    id: NotRequired[str]
    name: NotRequired[str]
    auth_token: NotRequired[str]
    url: NotRequired[str]
    created_at: NotRequired[datetime.datetime]
    updated_at: NotRequired[datetime.datetime]

def get_fake_webhook(fields: WebhookDict | None = None) -> models.Webhook:
    if fields is None:
        fields = WebhookDict()

    return models.Webhook(
        id=fields.get("id", str(fake.uuid4())),
        name=fields.get("name", fake.name()),
        auth_token=fields.get("auth_token", cast(str, fake.uuid4())),
        url=fields.get("url", fake.url()),
        created_at=fields.get("created_at", datetime.datetime.now()),
        updated_at=fields.get("updated_at", datetime.datetime.now()),
    )

def create_fake_webhook(db: Session, fields: WebhookDict | None = None) -> models.Webhook:
    return create_fake_object(db, get_fake_webhook, fields)

async def create_fake_webhook_async(db: AsyncSession, fields: WebhookDict | None = None) -> models.Webhook:
    return await create_fake_object_async(db, get_fake_webhook, fields)

def create_fake_object(db: Session, fn: Callable[[Any], T], fields: Any | None = None) -> T:
    obj = fn(fields)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

async def create_fake_object_async(db: AsyncSession, fn: Callable[[Any], T], fields: Any | None = None) -> T:
    obj = fn(fields)
    async with db as session:
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
    return obj
