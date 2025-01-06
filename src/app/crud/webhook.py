from typing import Any, cast
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.webhook import Webhook as WebhookModel
from ..schemas.webhook import Webhook as WebhookSchema
from ..schemas.webhook import WebhookCreate, WebhookUpdate
from .base import BaseCRUD


class WebhookCRUD(BaseCRUD[WebhookSchema, WebhookModel]):
    def model_to_schema(self, model: WebhookModel) -> WebhookSchema:
        model_dump = {
            "id": model.id,
            "name": model.name,
            "url": model.url,
            "auth_token": model.auth_token,
            "created_at": model.created_at,
            "updated_at": model.updated_at,
        }
        return WebhookSchema.model_validate(model_dump)

    async def read(self, id: str, allow_none: bool = True) -> WebhookSchema | None:
        query = select(WebhookModel).where(WebhookModel.id == id)

        result = await self.db.execute(query)

        webhook = result.scalar_one_or_none()
        if not webhook and not allow_none:
            raise HTTPException(status_code=404, detail="Webhook not found")

        return self.model_to_schema(webhook) if webhook else None

    async def create(self, data: WebhookCreate) -> WebhookSchema:
        webhook = WebhookModel(**data.model_dump())

        auth_token = str(uuid4())
        webhook.auth_token = auth_token

        self.db.add(webhook)
        await self.db.commit()
        await self.db.refresh(webhook)

        return self.model_to_schema(webhook)

    async def list(self, **kwargs: Any) -> list[WebhookSchema]:
        webhooks_pydantic: list[WebhookSchema] = []
        webhooks = await self.db.execute(select(WebhookModel))
        for webhook in webhooks:
            webhook_pydantic = self.model_to_schema(webhook[0])
            webhooks_pydantic.append(webhook_pydantic)
        return webhooks_pydantic

    async def update(self, id: str, data: WebhookUpdate) -> WebhookSchema:
        webhook = await self.check_exists(id)

        new_webhook = self.update_object(webhook, data)

        await self.db.commit()
        await self.db.refresh(new_webhook)
        return self.model_to_schema(new_webhook)

    async def delete(self, id: str):
        webhook = await self.check_exists(id)

        await self.db.delete(webhook)
        await self.db.commit()
