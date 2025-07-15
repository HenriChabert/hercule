import datetime
from typing import NotRequired, TypedDict, TypeVar, cast

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import Session

from src.app import models
from src.app.core.db.database import Base

from .base import BaseFaker

T = TypeVar("T", bound=Base)


class WebhookFields(BaseModel):
    id: str | None = None
    name: str | None = None
    auth_token: str | None = None
    url: str | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None


class WebhookFaker(BaseFaker[models.Webhook]):
    def get_fake(self, fields: WebhookFields | None = None) -> models.Webhook:
        if fields is None:
            fields = WebhookFields()

        return models.Webhook(
            id=fields.id or str(self.fake.uuid4()),
            name=fields.name or self.fake.name(),
            auth_token=fields.auth_token or cast(str, self.fake.uuid4()),
            url=fields.url or self.fake.url(),
            created_at=fields.created_at or datetime.datetime.now(),
            updated_at=fields.updated_at or datetime.datetime.now(),
        )

    async def create_fake(
        self, db: AsyncSession, fields: WebhookFields | None = None
    ) -> models.Webhook:
        return await self.create_fake_object(db, self.get_fake, fields)
