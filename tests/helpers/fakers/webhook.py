import datetime
from typing import NotRequired, TypedDict, TypeVar, cast

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import Session

from src.app import models
from src.app.core.db.database import Base

from .base import BaseFaker

T = TypeVar("T", bound=Base)

class WebhookFields(TypedDict):
    id: NotRequired[str]
    name: NotRequired[str]
    auth_token: NotRequired[str]
    url: NotRequired[str]
    created_at: NotRequired[datetime.datetime]
    updated_at: NotRequired[datetime.datetime]

class WebhookFaker(BaseFaker[models.Webhook]):
    def get_fake(self, fields: WebhookFields | None = None) -> models.Webhook:
        if fields is None:
            fields = WebhookFields()

        return models.Webhook(
            id=fields.get("id", str(self.fake.uuid4())),
            name=fields.get("name", self.fake.name()),
            auth_token=fields.get("auth_token", cast(str, self.fake.uuid4())),
            url=fields.get("url", self.fake.url()),
            created_at=fields.get("created_at", datetime.datetime.now()),
            updated_at=fields.get("updated_at", datetime.datetime.now()),
        )

    async def create_fake(self, db: AsyncSession, fields: WebhookFields | None = None) -> models.Webhook:
        return await self.create_fake_object(db, self.get_fake, fields)