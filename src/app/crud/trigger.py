from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.trigger import Trigger
from ..schemas.trigger import TriggerCreate, TriggerRead, TriggerUpdate

class TriggerCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: TriggerCreate) -> TriggerRead:
        trigger = Trigger(**data.model_dump())
        self.db.add(trigger)
        await self.db.commit()
        await self.db.refresh(trigger)
        return TriggerRead.model_validate(trigger)

    async def read(self, trigger_id: str) -> TriggerRead:
        trigger = await self.db.get(Trigger, trigger_id)
        if not trigger:
            raise HTTPException(status_code=404, detail="Trigger not found")
        return TriggerRead.model_validate(trigger)

    async def list(self) -> list[TriggerRead]:
        triggers = await self.db.execute(select(Trigger))
        return [TriggerRead.model_validate(trigger) for trigger in triggers]


    async def update(self, trigger_id: str, data: TriggerUpdate) -> TriggerRead:
        trigger = await self.db.get(Trigger, trigger_id)
        if not trigger:
            raise HTTPException(status_code=404, detail="Trigger not found")
        trigger.name = data.name
        await self.db.commit()
        await self.db.refresh(trigger)
        return TriggerRead.model_validate(trigger)


    async def delete(self, trigger_id: str):
        trigger = await self.db.get(Trigger, trigger_id)
        if not trigger:
            raise HTTPException(status_code=404, detail="Trigger not found")
        await self.db.delete(trigger)
        await self.db.commit()
