from typing import Annotated, Any, Mapping

from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.dependencies import check_secret_key_header
from src.app.controllers.trigger import TriggerController
from src.app.core.db.database import async_get_db
from src.app.schemas.trigger import TriggerCreateClient, TriggerUpdate
from src.app.types.events import EventContext, EventType

router = APIRouter(tags=["trigger"], dependencies=[Depends(check_secret_key_header)])


@router.post("/trigger", status_code=status.HTTP_201_CREATED)
async def create_trigger(
    trigger: TriggerCreateClient, db: Annotated[AsyncSession, Depends(async_get_db)]
):
    trigger_ctrl = TriggerController(db)
    return await trigger_ctrl.create(trigger)


@router.get("/trigger/{trigger_id}")
async def get_trigger(
    trigger_id: str, db: Annotated[AsyncSession, Depends(async_get_db)]
):
    trigger_ctrl = TriggerController(db)
    return await trigger_ctrl.read(trigger_id, raise_exception=True)


@router.get("/triggers")
async def get_triggers(
    db: Annotated[AsyncSession, Depends(async_get_db)], event: EventType | None = None
):
    trigger_ctrl = TriggerController(db)
    return await trigger_ctrl.list(event=event)


@router.put("/trigger/{trigger_id}")
async def update_trigger(
    trigger_id: str,
    trigger: TriggerUpdate,
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    trigger_ctrl = TriggerController(db)
    return await trigger_ctrl.update(trigger_id, trigger)


@router.delete("/trigger/{trigger_id}")
async def delete_trigger(
    trigger_id: str, db: Annotated[AsyncSession, Depends(async_get_db)]
):
    trigger_ctrl = TriggerController(db)
    return await trigger_ctrl.delete(trigger_id)


@router.post("/trigger/{trigger_id}/run")
async def run_trigger(
    trigger_id: str,
    event: Annotated[EventType, Body()],
    context: Annotated[EventContext, Body()],
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    trigger_ctrl = TriggerController(db)
    return await trigger_ctrl.trigger(trigger_id, event, context)


@router.post("/triggers/event")
async def trigger_event(
    event: Annotated[EventType, Body()],
    context: Annotated[EventContext, Body()],
    web_push_subscription: Annotated[dict[str, Any], Body()],
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    trigger_ctrl = TriggerController(db)
    events_results = await trigger_ctrl.trigger_event(
        event=event, context=context, web_push_subscription=web_push_subscription
    )
    return events_results
