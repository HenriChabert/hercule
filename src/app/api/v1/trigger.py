from fastapi import APIRouter, status

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from typing import Annotated

from src.app.schemas.trigger import TriggerCreate, TriggerUpdate
from src.app.controllers.trigger import TriggerController
from src.app.core.db.database import async_get_db

router = APIRouter(tags=["trigger"])

@router.post("/trigger", status_code=status.HTTP_201_CREATED)
async def create_trigger(trigger: TriggerCreate, db: Annotated[AsyncSession, Depends(async_get_db)]):
    trigger_ctrl = TriggerController(db)
    return await trigger_ctrl.create(trigger)

@router.get("/trigger/{trigger_id}")
async def get_trigger(trigger_id: str, db: Annotated[AsyncSession, Depends(async_get_db)]):
    trigger_ctrl = TriggerController(db)
    return await trigger_ctrl.read(trigger_id, raise_exception=True)
    
@router.get("/triggers")
async def get_triggers(db: Annotated[AsyncSession, Depends(async_get_db)]):
    trigger_ctrl = TriggerController(db)
    return await trigger_ctrl.list()    

@router.put("/trigger/{trigger_id}")
async def update_trigger(trigger_id: str, trigger: TriggerUpdate, db: Annotated[AsyncSession, Depends(async_get_db)]):
    trigger_ctrl = TriggerController(db)
    return await trigger_ctrl.update(trigger_id, trigger)

@router.delete("/trigger/{trigger_id}")
async def delete_trigger(trigger_id: str, db: Annotated[AsyncSession, Depends(async_get_db)]):
    trigger_ctrl = TriggerController(db)
    return await trigger_ctrl.delete(trigger_id)