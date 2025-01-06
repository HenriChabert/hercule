from typing import Any, cast

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.webhook_usage import WebhookUsage as WebhookUsageModel
from ..models.webhook_usage import WebhookUsageStatus
from ..schemas.webhook_usage import WebhookUsage as WebhookUsageSchema
from ..schemas.webhook_usage import WebhookUsageCreate, WebhookUsageUpdate
from .base import BaseCRUD


class WebhookUsageCRUD(BaseCRUD[WebhookUsageSchema, WebhookUsageModel]):
    def model_to_schema(self, model: WebhookUsageModel) -> WebhookUsageSchema:
        model_dump = {
            "id": model.id,
            "webhook_id": model.webhook_id,
            "event": model.event,
            "status": model.status,
        }
        return WebhookUsageSchema.model_validate(model_dump)

    async def create(self, data: WebhookUsageCreate) -> WebhookUsageSchema:
        webhook_usage = WebhookUsageModel(**data.model_dump())
        self.db.add(webhook_usage)
        await self.db.commit()
        await self.db.refresh(webhook_usage)
        return self.model_to_schema(webhook_usage)

    async def read(
        self, id: str, allow_none: bool = False
    ) -> WebhookUsageSchema | None:
        query = select(WebhookUsageModel).where(WebhookUsageModel.id == id)

        result = await self.db.execute(query)

        webhook_usage = result.scalar_one_or_none()
        if not webhook_usage and not allow_none:
            raise HTTPException(status_code=404, detail="Webhook usage not found")

        return self.model_to_schema(webhook_usage) if webhook_usage else None

    async def list(
        self, webhook_id: str | None = None, **kwargs: Any
    ) -> list[WebhookUsageSchema]:
        query = select(WebhookUsageModel)
        if webhook_id:
            query = query.where(WebhookUsageModel.webhook_id == webhook_id)

        result = await self.db.execute(query)

        return [
            self.model_to_schema(webhook_usage)
            for webhook_usage in result.scalars().all()
        ]

    async def update(self, id: str, data: WebhookUsageUpdate) -> WebhookUsageSchema:
        webhook_usage = await self.check_exists(id)

        new_webhook_usage = self.update_object(webhook_usage, data)

        await self.db.commit()
        await self.db.refresh(new_webhook_usage)
        return self.model_to_schema(new_webhook_usage)

    async def delete(self, id: str):
        webhook_usage = await self.check_exists(id)
        await self.db.delete(webhook_usage)
        await self.db.commit()

    async def update_status(
        self, id: str, status: WebhookUsageStatus
    ) -> WebhookUsageSchema:
        await self.check_exists(id)

        query = (
            update(WebhookUsageModel)
            .where(WebhookUsageModel.id == id)
            .values(status=status)
        )
        await self.db.execute(query)
        await self.db.commit()

        return cast(WebhookUsageSchema, await self.read(id))
