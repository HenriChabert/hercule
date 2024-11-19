import uuid as uuid_pkg
import datetime
from sqlalchemy.orm import Session
from typing import cast, TypedDict, NotRequired
from src.app import models
from src.app import schemas
from tests.conftest import fake

class TriggerDict(TypedDict):
    id: NotRequired[uuid_pkg.UUID]
    name: NotRequired[str]
    webhook_id: NotRequired[uuid_pkg.UUID]
    created_at: NotRequired[datetime.datetime]
    updated_at: NotRequired[datetime.datetime]

def get_fake_trigger(fields: TriggerDict | None = None) -> models.Trigger:
    if fields is None:
        fields = TriggerDict()

    return models.Trigger(
        id=fields.get("id", cast(uuid_pkg.UUID, fake.uuid4())),
        name=fields.get("name", fake.name()),
        webhook_id=fields.get("webhook_id", cast(uuid_pkg.UUID, fake.uuid4()))
    )

def create_fake_trigger(db: Session, fields: TriggerDict | None = None) -> models.Trigger:
    trigger = get_fake_trigger(fields)
    db.add(trigger)
    db.commit()
    db.refresh(trigger)
    return trigger
    