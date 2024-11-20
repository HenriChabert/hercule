from uuid import uuid4
from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.webhook import Webhook as WebhookSchema, WebhookCreate, WebhookUpdate
from ..models.webhook import Webhook as WebhookModel
from .base import BaseCRUD
from typing import Any


class WebhookCRUD(BaseCRUD[WebhookSchema, WebhookModel]):
    def __init__(self, db: AsyncSession):
        self.db = db

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

    async def create(self, data: WebhookCreate) -> WebhookSchema:
        webhook = WebhookModel(**data.model_dump())

        auth_token = str(uuid4())
        webhook.auth_token = auth_token

        self.db.add(webhook)
        await self.db.commit()
        await self.db.refresh(webhook)

        return self.model_to_schema(webhook)

    async def read(self, id: str, raise_exception: bool = False) -> WebhookSchema | None:
        webhook = await self.db.get(WebhookModel, id)
        if not webhook and raise_exception:
            raise HTTPException(status_code=404, detail="Webhook not found")
        
        return self.model_to_schema(webhook) if webhook else None

    async def list(self, **kwargs: Any) -> list[WebhookSchema]:
        webhooks_pydantic: list[WebhookSchema] = []
        webhooks = await self.db.execute(select(WebhookModel))
        for webhook in webhooks:
            webhook_pydantic = self.model_to_schema(webhook[0])
            webhooks_pydantic.append(webhook_pydantic)
        return webhooks_pydantic

    async def update(self, id: str, data: WebhookUpdate) -> WebhookSchema:
        webhook = await self.db.get(WebhookModel, id)
        if not webhook:
            raise HTTPException(status_code=404, detail="Webhook not found")
        
        provided_params = self.only_provided_params(data)
        for key, value in provided_params.items():
            if hasattr(webhook, key):
                setattr(webhook, key, value)

        await self.db.commit()
        await self.db.refresh(webhook)
        return self.model_to_schema(webhook)

    async def delete(self, id: str):
        webhook = await self.db.get(WebhookModel, id)
        if not webhook:
            raise HTTPException(status_code=404, detail="Webhook not found")
        await self.db.delete(webhook)
        await self.db.commit()
    