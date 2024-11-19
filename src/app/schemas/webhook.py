from typing import Annotated

from pydantic import BaseModel, Field

from ..core.schemas import TimestampSchema, UUIDSchema

name_field = Field(..., description="The name of the webhook", examples=["My Webhook"])
url_field = Field(..., description="The URL of the webhook", pattern=r"^https?://.*$", examples=["https://example.com"])
auth_token_field = Field(..., description="The auth token of the webhook", examples=["sijwdnu3"])

class WebhookBase(BaseModel):
    name: Annotated[str, name_field]
    url: Annotated[str, url_field]

class Webhook(WebhookBase, UUIDSchema, TimestampSchema):
    pass

class WebhookRead(Webhook):
    pass

class WebhookReadSecured(Webhook):
    auth_token: Annotated[str, auth_token_field]

class WebhookCreate(WebhookBase):
    auth_token: Annotated[str, auth_token_field]

class WebhookUpdate(WebhookBase):
    url: Annotated[str, url_field]

class WebhookDelete(UUIDSchema):
    pass

