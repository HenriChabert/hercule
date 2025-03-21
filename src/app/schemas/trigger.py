from functools import wraps
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from src.app.core.schemas import IDSchema, TimestampSchema
from src.app.models.trigger import TriggerSource
from src.app.types.events import EventType


@wraps(Field)
def url_regex_field_factory(**kwargs: Any):
    return Field(
        description="The URL regex of the trigger",
        examples=[".*", "https://example.com", "https://example.com/.*"],
        **kwargs
    )


@wraps(Field)
def name_field_factory(**kwargs: Any):
    return Field(
        description="The name of the trigger", examples=["My Trigger"], **kwargs
    )


@wraps(Field)
def webhook_id_field_factory(**kwargs: Any):
    return Field(description="The ID of the webhook", examples=[str(uuid4())], **kwargs)


@wraps(Field)
def source_field_factory(**kwargs: Any):
    return Field(
        description="The source of the trigger", examples=["n8n", "zapier"], **kwargs
    )


@wraps(Field)
def event_field_factory(**kwargs: Any):
    return Field(
        description="The event triggering the trigger",
        examples=["page_created", "button_clicked"],
        **kwargs
    )


class TriggerBase(BaseModel):
    model_config = {"from_attributes": False}
    webhook_id: str | None = webhook_id_field_factory(default=None)
    url_regex: str | None = url_regex_field_factory(default=".*")
    source: TriggerSource = source_field_factory(default="n8n")
    event: EventType = event_field_factory(default="button_clicked")
    name: str = name_field_factory()


class Trigger(TriggerBase, IDSchema, TimestampSchema):
    pass


class TriggerRead(Trigger):
    pass


class TriggerCreateClient(TriggerBase):
    webhook_id: str | None = webhook_id_field_factory(default=None)
    webhook_url: str | None = Field(description="The URL of the webhook", default=None)


class TriggerCreate(TriggerBase):
    webhook_id: str | None = webhook_id_field_factory(default=None)


class TriggerUpdate(BaseModel):
    url_regex: str | None = url_regex_field_factory(default=None)
    name: str | None = name_field_factory(default=None)
    event: str | None = event_field_factory(default=None)
