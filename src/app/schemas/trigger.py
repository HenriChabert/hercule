from uuid import uuid4
from typing import Annotated, Any
from functools import wraps
from pydantic import BaseModel, Field
from ..core.schemas import TimestampSchema, IDSchema
from ..core.sentinel import NOT_PROVIDED
from ..models.trigger import TriggerSource

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

class TriggerBase(BaseModel):
    model_config = {
        "from_attributes": False
    }
    webhook_id: Annotated[str, webhook_id_field_factory()]
    url_regex: Annotated[str, url_regex_field_factory(default=".*")]
    source: Annotated[TriggerSource, source_field_factory(default="n8n")]
    name: Annotated[str, name_field_factory()]

class Trigger(TriggerBase, IDSchema, TimestampSchema):
    pass

class TriggerRead(Trigger):
    pass

class TriggerCreate(TriggerBase):
    pass

class TriggerUpdate(BaseModel):
    url_regex: Annotated[str, url_regex_field_factory(default=NOT_PROVIDED)]
    name: Annotated[str, name_field_factory(default=NOT_PROVIDED)]