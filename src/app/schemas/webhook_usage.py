from functools import wraps
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from src.app.types.actions import Action

from ..core.schemas import IDSchema, TimestampSchema
from ..models.webhook_usage import WebhookUsageStatus
from ..types.events import EventType


@wraps(Field)
def webhook_id_field_factory(**kwargs: Any):
    return Field(description="The ID of the webhook", examples=[str(uuid4())], **kwargs)


@wraps(Field)
def event_field_factory(**kwargs: Any):
    return Field(
        description="The event triggering the trigger",
        examples=["page_created", "button_clicked"],
        **kwargs
    )


@wraps(Field)
def status_field_factory(**kwargs: Any):
    return Field(
        description="The status of the webhook usage",
        examples=["success", "failure"],
        **kwargs
    )


@wraps(Field)
def webpush_subscription_data_field_factory(**kwargs: Any):
    return Field(
        description="The webpush subscription data",
        examples=[
            {
                "endpoint": "https://example.com/webpush",
                "keys": {"p256dh": "BGoQYQ==", "auth": "1234567890"},
            }
        ],
        **kwargs
    )


class WebhookUsageBase(BaseModel):
    model_config = {"from_attributes": False}

    webhook_id: str = webhook_id_field_factory()
    event: EventType = event_field_factory()
    status: WebhookUsageStatus = status_field_factory(default="pending")
    webpush_subscription_data: dict[str, Any] | None = (
        webpush_subscription_data_field_factory(default=None)
    )


class WebhookUsage(WebhookUsageBase, IDSchema, TimestampSchema):
    pass


class WebhookUsageRead(WebhookUsage):
    pass


class WebhookUsageCreate(WebhookUsageBase):
    pass


class WebhookUsageUpdate(BaseModel):
    status: WebhookUsageStatus | None = status_field_factory(default=None)


class WebhookUsageCallbackPayload(BaseModel):
    action: Action = Field(description="The action to be performed")
