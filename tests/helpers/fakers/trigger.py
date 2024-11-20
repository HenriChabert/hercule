import datetime
from sqlalchemy.orm import Session
from typing import cast, TypedDict, NotRequired
from src.app import models
from .base import BaseFaker
from .webhook import WebhookFaker, WebhookFields


class TriggerFields(TypedDict):
    id: NotRequired[str]
    name: NotRequired[str]
    webhook_id: NotRequired[str]
    created_at: NotRequired[datetime.datetime]
    updated_at: NotRequired[datetime.datetime]

class TriggerFaker(BaseFaker[models.Trigger]):
    def get_fake(self, fields: TriggerFields | None = None) -> models.Trigger:
        if fields is None:
            fields = TriggerFields()

        return models.Trigger(
            id=fields.get("id", str(self.fake.uuid4())),
            name=fields.get("name", self.fake.name()),
            webhook_id=fields.get("webhook_id", str(self.fake.uuid4()))
        )

    def create_fake(self, db: Session, fields: TriggerFields | None = None) -> models.Trigger:
        webhook_faker = WebhookFaker()
        webhook_fields = None
        if fields and "webhook_id" in fields:
            webhook_fields = WebhookFields(id=fields["webhook_id"])
        webhook = webhook_faker.create_fake(db, webhook_fields)

        if fields is None:
            fields = TriggerFields(
                webhook_id=webhook.id
            )
        else:
            fields["webhook_id"] = webhook.id

        return self.create_fake_object(db, self.get_fake, fields)
    