import datetime
import random as rd
from typing import NotRequired, TypedDict, cast

from sqlalchemy.ext.asyncio import AsyncSession

from src.app import models
from src.app.models.trigger import EventType, TriggerSource

from .base import BaseFaker
from .webhook import WebhookFaker, WebhookFields


class TriggerFields(TypedDict):
    id: NotRequired[str]
    name: NotRequired[str]
    webhook_id: NotRequired[str]
    source: NotRequired[TriggerSource]
    event: NotRequired[EventType]
    created_at: NotRequired[datetime.datetime]
    updated_at: NotRequired[datetime.datetime]


class TriggerFaker(BaseFaker[models.Trigger]):
    def get_fake(self, fields: TriggerFields | None = None) -> models.Trigger:
        if fields is None:
            fields = TriggerFields()

        return models.Trigger(
            id=fields.get("id", str(self.fake.uuid4())),
            name=fields.get("name", self.fake.name()),
            source=fields.get("source", "n8n"),
            url_regex=fields.get("url_regex", ".*"),
            event=fields.get("event", rd.choice(["page_opened", "button_clicked"])),
            webhook_id=fields.get("webhook_id", str(self.fake.uuid4())),
        )

    async def create_fake(
        self, db: AsyncSession, fields: TriggerFields | None = None
    ) -> models.Trigger:
        webhook_faker = WebhookFaker()
        if fields is None:
            fields = TriggerFields()

        if not "webhook_id" in fields:
            webhook = await webhook_faker.create_fake(db, WebhookFields())
            fields["webhook_id"] = webhook.id

        new_trigger = await self.create_fake_object(db, self.get_fake, fields)

        return new_trigger
