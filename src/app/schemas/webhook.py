from typing import Any
from functools import wraps
import datetime

from pydantic import BaseModel, Field

from ..core.schemas import TimestampSchema, IDSchema
from ..core.sentinel import NOT_PROVIDED



@wraps(Field)
def name_field_factory(**kwargs: Any):
    return Field(description="The name of the webhook", examples=["My Webhook"], **kwargs)

@wraps(Field)
def url_field_factory(**kwargs: Any):
    return Field(description="The URL of the webhook", pattern=r"^https?://.*$", examples=["https://example.com"], **kwargs)

@wraps(Field)
def auth_token_field_factory(**kwargs: Any):
    return Field(description="The auth token of the webhook", examples=["sijwdnu3"], **kwargs)

class WebhookBase(BaseModel):
    model_config = {
        "from_attributes": False
    }

    name: str = name_field_factory(default_factory=lambda: f"Webhook created at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    url: str = url_field_factory()

class WebhookBaseSecured(WebhookBase):
    auth_token: str = auth_token_field_factory()

class Webhook(WebhookBaseSecured, IDSchema, TimestampSchema):
    pass

class WebhookUnsafe(WebhookBase, IDSchema, TimestampSchema):
    pass

class WebhookRead(WebhookUnsafe):
    pass
    
class WebhookReadSecured(Webhook):
    pass

class WebhookCreate(WebhookBase):
    pass

class WebhookUpdate(BaseModel):
    name: str = name_field_factory(default=NOT_PROVIDED)
    url: str = url_field_factory(default=NOT_PROVIDED)