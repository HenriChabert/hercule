from fastapi import HTTPException
from typing import Mapping, Any, overload, Literal
from src.app.controllers.base import BaseController
from src.app.controllers.webhook import WebhookController
from src.app.core.sentinel import NOT_PROVIDED
from src.app.schemas.trigger import TriggerCreateClient, TriggerCreate, Trigger as TriggerSchema, TriggerUpdate
from src.app.schemas.webhook import WebhookCreate
from src.app.models.trigger import Trigger as TriggerModel
from src.app.crud.trigger import TriggerCRUD

from sqlalchemy.ext.asyncio import AsyncSession

class TriggerController(BaseController[TriggerSchema, TriggerModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.crud = TriggerCRUD(db)

    async def create(self, trigger: TriggerCreateClient) -> TriggerSchema:
        webhook_ctrl = WebhookController(self.db)
        
        if trigger.webhook_url != NOT_PROVIDED:
            webhook = await webhook_ctrl.create(
                WebhookCreate(url=trigger.webhook_url)
            )
            trigger.webhook_id = webhook.id

        try:
            _ = await webhook_ctrl.read(trigger.webhook_id, raise_exception=True)
        except HTTPException as e:
            raise HTTPException(status_code=422, detail="Webhook should exist") from e
        
        trigger_dto = TriggerCreate(**trigger.model_dump(exclude={"webhook_url"}))
        
        return await self.crud.create(trigger_dto)
    
    @overload
    async def read(self, trigger_id: str, raise_exception: Literal[False] = False) -> TriggerSchema | None: ...

    @overload
    async def read(self, trigger_id: str, raise_exception: Literal[True]) -> TriggerSchema: ...

    async def read(self, trigger_id: str, raise_exception: bool = False) -> TriggerSchema | None:
        return await self.crud.read(trigger_id, raise_exception)
    
    async def list(self) -> list[TriggerSchema]:
        return await self.crud.list()
    
    async def update(self, trigger_id: str, trigger: TriggerUpdate) -> TriggerSchema:
        return await self.crud.update(trigger_id, trigger)
    
    async def delete(self, trigger_id: str) -> None:
        return await self.crud.delete(trigger_id)
    
    async def trigger(self, trigger_id: str, payload: Mapping[str, Any]) -> None:
        trigger = await self.read(trigger_id, raise_exception=True)
        webhook_ctrl = WebhookController(self.db)
        return await webhook_ctrl.call(trigger.webhook_id, payload)
