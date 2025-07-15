import datetime
import random as rd
from typing import NotRequired, TypedDict, cast

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.app import models
from src.app.models.trigger import EventType, TriggerSource

from .base import BaseFaker
from .webhook import WebhookFaker, WebhookFields


class TriggerFields(BaseModel):
    id: str | None = None
    name: str | None = None
    webhook_id: str | None = None
    source: TriggerSource | None = None
    event: EventType | None = None
    url_regex: str | None = None
    user_id: str | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None


class TriggerFaker(BaseFaker[models.Trigger]):
    def get_fake(self, fields: TriggerFields | None = None) -> models.Trigger:
        if fields is None:
            fields = TriggerFields()

        return models.Trigger(
            id=fields.id or str(self.fake.uuid4()),
            name=fields.name or self.fake.name(),
            source=fields.source or "n8n",
            url_regex=fields.url_regex or ".*",
            user_id=fields.user_id or None,
            event=fields.event or rd.choice(["page_opened", "button_clicked"]),
            webhook_id=fields.webhook_id or str(self.fake.uuid4()),
        )

    async def create_fake(
        self, db: AsyncSession, fields: TriggerFields | None = None
    ) -> models.Trigger:
        webhook_faker = WebhookFaker()
        if fields is None:
            fields = TriggerFields()

        if fields.webhook_id is None:
            webhook = await webhook_faker.create_fake(db, WebhookFields())
            fields.webhook_id = webhook.id

        new_trigger = await self.create_fake_object(db, self.get_fake, fields)

        return new_trigger
