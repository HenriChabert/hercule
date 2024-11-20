from src.app.controllers.base import BaseController
from src.app.schemas.webhook import WebhookCreate, Webhook as WebhookSchema, WebhookUpdate
from src.app.models.webhook import Webhook as WebhookModel

from sqlalchemy.ext.asyncio import AsyncSession
from src.app.crud.webhook import WebhookCRUD

class WebhookController(BaseController[WebhookSchema, WebhookModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.crud = WebhookCRUD(db)

    async def create(self, webhook: WebhookCreate) -> WebhookSchema:
        return await self.crud.create(webhook)

    async def read(self, webhook_id: str, raise_exception: bool = False) -> WebhookSchema | None:
        webhook = await self.crud.read(webhook_id, raise_exception=raise_exception)
        return webhook
    
    async def list(self) -> list[WebhookSchema]:
        return await self.crud.list()
    
    async def update(self, webhook_id: str, webhook: WebhookUpdate) -> WebhookSchema:
        return await self.crud.update(webhook_id, webhook)
    
    async def delete(self, webhook_id: str) -> None:
        return await self.crud.delete(webhook_id)