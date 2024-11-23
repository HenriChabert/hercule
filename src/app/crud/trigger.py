from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.sentinel import NOT_PROVIDED
from src.app.schemas.webhook import WebhookCreate, WebhookBase

from ..models.trigger import Trigger as TriggerModel
from ..schemas.trigger import Trigger as TriggerSchema, TriggerCreate, TriggerUpdate, TriggerCreateClient
from ..types.events import EventType
from .base import BaseCRUD
from .webhook import WebhookCRUD

from typing import Any

class TriggerCRUD(BaseCRUD[TriggerSchema, TriggerModel]):
    def __init__(self, db: AsyncSession):
        self.db = db

    def model_to_schema(self, model: TriggerModel) -> TriggerSchema:
        model_dump = {
            "id": model.id,
            "name": model.name,
            "source": model.source,
            "url_regex": model.url_regex,
            "event": model.event,
            "webhook_id": model.webhook_id,
            "created_at": model.created_at,
            "updated_at": model.updated_at,
        }
        return TriggerSchema.model_validate(model_dump)

    async def create(self, data: TriggerCreate) -> TriggerSchema:
        trigger = TriggerModel(**data.model_dump())
        self.db.add(trigger)
        await self.db.commit()
        await self.db.refresh(trigger)
        return self.model_to_schema(trigger)

    async def read(self, id: str, raise_exception: bool = False) -> TriggerSchema | None:
        trigger = await self.db.get(TriggerModel, id)
        if not trigger and raise_exception:
            raise HTTPException(status_code=404, detail="Trigger not found")
        return self.model_to_schema(trigger) if trigger else None

    async def list(self, event: EventType | None = None, **kwargs: Any) -> list[TriggerSchema]:
        query = select(TriggerModel)
        if event:
            query = query.where(TriggerModel.event == event)

        triggers = await self.db.execute(query)
        
        return [self.model_to_schema(trigger[0]) for trigger in triggers]


    async def update(self, id: str, data: TriggerUpdate) -> TriggerSchema:
        trigger = await self.db.get(TriggerModel, id)
        if not trigger:
            raise HTTPException(status_code=404, detail="Trigger not found")
        
        provided_params = self.only_provided_params(data)
        for key, value in provided_params.items():
            if hasattr(trigger, key):
                setattr(trigger, key, value)

        await self.db.commit()
        await self.db.refresh(trigger)
        return self.model_to_schema(trigger)


    async def delete(self, id: str):
        trigger = await self.db.get(TriggerModel, id)
        if not trigger:
            raise HTTPException(status_code=404, detail="Trigger not found")
        await self.db.delete(trigger)
        await self.db.commit()
