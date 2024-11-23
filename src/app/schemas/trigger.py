from uuid import uuid4
from typing import  Any
from functools import wraps
from pydantic import BaseModel, Field
from ..core.schemas import TimestampSchema, IDSchema
from ..core.sentinel import NOT_PROVIDED
from ..models.trigger import TriggerSource
from ..types.events import EventType
@wraps(Field)
def url_regex_field_factory(**kwargs: Any):
    return Field(description="The URL regex of the trigger", examples=[".*", "https://example.com", "https://example.com/.*"], **kwargs)

@wraps(Field)
def name_field_factory(**kwargs: Any):
    return Field(description="The name of the trigger", examples=["My Trigger"], **kwargs)

@wraps(Field)
def webhook_id_field_factory(**kwargs: Any):
    return Field(description="The ID of the webhook", examples=[str(uuid4())], **kwargs)

@wraps(Field)
def source_field_factory(**kwargs: Any):
    return Field(description="The source of the trigger", examples=["n8n", "zapier"], **kwargs)

@wraps(Field)
def event_field_factory(**kwargs: Any):
    return Field(description="The event triggering the trigger", examples=["page_created", "button_clicked"], **kwargs)

class TriggerBase(BaseModel):
    model_config = {
        "from_attributes": False
    }
    webhook_id: str = webhook_id_field_factory()
    url_regex: str = url_regex_field_factory(default=".*")
    source: TriggerSource = source_field_factory(default="n8n")
    event: EventType = event_field_factory(default="button_clicked")
    name: str = name_field_factory()

class Trigger(TriggerBase, IDSchema, TimestampSchema):
    pass

class TriggerRead(Trigger):
    pass

class TriggerCreateClient(TriggerBase):
    webhook_id: str = webhook_id_field_factory(default=NOT_PROVIDED)
    webhook_url: str = Field(description="The URL of the webhook", default=NOT_PROVIDED)

class TriggerCreate(TriggerBase):
    webhook_id: str = webhook_id_field_factory(default=NOT_PROVIDED)

class TriggerUpdate(BaseModel):
    url_regex: str = url_regex_field_factory(default=NOT_PROVIDED)
    name: str = name_field_factory(default=NOT_PROVIDED)
    event: str = event_field_factory(default=NOT_PROVIDED)
