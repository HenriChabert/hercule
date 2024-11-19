from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.webhook import WebhookCreate, WebhookUpdate, WebhookRead
from ..models.webhook import Webhook


class WebhookCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: WebhookCreate) -> WebhookRead:
        webhook = Webhook(**data.model_dump())
        self.db.add(webhook)
        await self.db.commit()
        await self.db.refresh(webhook)
        return WebhookRead(
            id=webhook.id,
            name=webhook.name,
            url=webhook.url,
            created_at=webhook.created_at,
            updated_at=webhook.updated_at,
        )

    async def read(self, webhook_id: str) -> WebhookRead:
        webhook = await self.db.get(Webhook, webhook_id)
        if not webhook:
            raise HTTPException(status_code=404, detail="Webhook not found")
        return WebhookRead.model_validate(webhook)

    async def list(self) -> list[WebhookRead]:
        webhooks = await self.db.execute(select(Webhook))
        return [WebhookRead.model_validate(webhook) for webhook in webhooks]

    async def update(self, webhook_id: str, data: WebhookUpdate) -> WebhookRead:
        webhook = await self.db.get(Webhook, webhook_id)
        if not webhook:
            raise HTTPException(status_code=404, detail="Webhook not found")
        webhook.name = data.name
        webhook.url = data.url
        await self.db.commit()
        await self.db.refresh(webhook)
        return WebhookRead.model_validate(webhook)

    async def delete(self, webhook_id: str):
        webhook = await self.db.get(Webhook, webhook_id)
        if not webhook:
            raise HTTPException(status_code=404, detail="Webhook not found")
        await self.db.delete(webhook)
        await self.db.commit()
    