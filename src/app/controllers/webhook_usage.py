import json
import logging
from typing import cast

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.controllers.base import BaseController
from src.app.core.config import settings
from src.app.crud.webhook_usage import WebhookUsageCRUD
from src.app.helpers.webpush import send_webpush
from src.app.models.webhook_usage import WebhookUsage as WebhookUsageModel
from src.app.models.webhook_usage import WebhookUsageStatus
from src.app.schemas.webhook_usage import WebhookUsage as WebhookUsageSchema
from src.app.schemas.webhook_usage import (
    WebhookUsageCallbackPayload,
    WebhookUsageCreate,
)

logger = logging.getLogger(__name__)


class WebhookUsageController(BaseController[WebhookUsageSchema, WebhookUsageModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.crud = WebhookUsageCRUD(db)

    async def create(self, webhook_usage: WebhookUsageCreate) -> WebhookUsageSchema:
        return await self.crud.create(webhook_usage)

    async def read(self, webhook_usage_id: str) -> WebhookUsageSchema | None:
        return await self.crud.read(webhook_usage_id)

    async def read_safe(self, webhook_usage_id: str) -> WebhookUsageSchema:
        return cast(
            WebhookUsageSchema, await self.crud.read(webhook_usage_id, allow_none=False)
        )
    
    async def update_status(self, webhook_usage_id: str, status: WebhookUsageStatus) -> WebhookUsageSchema:
        return await self.crud.update_status(webhook_usage_id, status)

    def get_callback_url(self, webhook_usage_id: str) -> str:
        return f"{settings.API_URL}/webhook-usage/{webhook_usage_id}/callback"

    async def callback(
        self, webhook_usage_id: str, payload: WebhookUsageCallbackPayload
    ) -> bool:
        webhook_usage = await self.read_safe(webhook_usage_id)

        webpush_sub_data = webhook_usage.webpush_subscription_data

        if not webpush_sub_data:
            raise HTTPException(
                status_code=400, detail="Invalid webpush subscription data"
            )

        await send_webpush(webpush_sub_data, payload.model_dump())
        
        return True
