from typing import Any, cast

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.trigger import Trigger as TriggerModel
from ..schemas.trigger import Trigger as TriggerSchema
from ..schemas.trigger import TriggerCreate, TriggerUpdate
from ..types.events import EventType
from .base import BaseCRUD


class TriggerCRUD(BaseCRUD[TriggerSchema, TriggerModel]):
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

    async def _read_orm(self, id: str, allow_none: bool = True) -> TriggerModel | None:
        query = select(TriggerModel).where(TriggerModel.id == id)

        result = await self.db.execute(query)

        trigger = result.scalar_one_or_none()
        if not trigger and not allow_none:
            raise HTTPException(status_code=404, detail="Trigger not found")

        return trigger

    async def create(self, data: TriggerCreate) -> TriggerSchema:
        trigger = TriggerModel(**data.model_dump())
        self.db.add(trigger)
        await self.db.commit()
        await self.db.refresh(trigger)
        return self.model_to_schema(trigger)

    async def list(
        self, event: EventType | None = None, **kwargs: Any
    ) -> list[TriggerSchema]:
        query = select(TriggerModel)
        if event:
            query = query.where(TriggerModel.event == event)

        result = await self.db.execute(query)

        return [self.model_to_schema(trigger) for trigger in result.scalars().all()]

    async def update(self, id: str, data: TriggerUpdate) -> TriggerSchema:
        trigger = await self._read_orm_safe(id)

        new_trigger = self.update_object(trigger, data)

        await self.db.commit()
        await self.db.refresh(new_trigger)
        return self.model_to_schema(new_trigger)

    async def delete(self, id: str):
        trigger = await self._read_orm_safe(id)
        await self.db.delete(trigger)
        await self.db.commit()
