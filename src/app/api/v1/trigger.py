from typing import Annotated, Any, Mapping

from fastapi import APIRouter, Body, Depends, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.dependencies import get_current_admin_user, get_current_user
from src.app.controllers.trigger import TriggerController
from src.app.core.db.database import async_get_db
from src.app.schemas.trigger import TriggerCreateClient, TriggerUpdate
from src.app.schemas.user import User as UserSchema
from src.app.types.events import EventContext, EventType

router = APIRouter(tags=["trigger"], dependencies=[Depends(get_current_user)])


@router.post("/trigger", status_code=status.HTTP_201_CREATED)
async def create_trigger(
    trigger: TriggerCreateClient,
    current_user: Annotated[UserSchema, Depends(get_current_admin_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    trigger_ctrl = TriggerController(db)
    return await trigger_ctrl.create(trigger)


@router.get("/trigger/{trigger_id}")
async def get_trigger(
    trigger_id: str,
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    trigger_ctrl = TriggerController(db)
    return await trigger_ctrl.read(trigger_id, allow_none=False)


@router.get("/triggers")
async def get_triggers(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    event: EventType | None = None,
    url: str | None = None,
):
    trigger_ctrl = TriggerController(db)
    return await trigger_ctrl.list(event=event, url=url)


@router.put("/trigger/{trigger_id}")
async def update_trigger(
    trigger_id: str,
    trigger: TriggerUpdate,
    current_user: Annotated[UserSchema, Depends(get_current_admin_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    trigger_ctrl = TriggerController(db)
    return await trigger_ctrl.update(trigger_id, trigger)


@router.delete("/trigger/{trigger_id}")
async def delete_trigger(
    trigger_id: str,
    current_user: Annotated[UserSchema, Depends(get_current_admin_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    trigger_ctrl = TriggerController(db)
    return await trigger_ctrl.delete(trigger_id)


class TriggerRunPayload(BaseModel):
    event: EventType
    context: EventContext
    web_push_subscription: dict[str, Any] | None = None


@router.post("/trigger/{trigger_id}/run")
async def run_trigger(
    trigger_id: str,
    payload: TriggerRunPayload,
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    trigger_ctrl = TriggerController(db)
    return await trigger_ctrl.trigger(
        trigger_id, payload.event, payload.context, payload.web_push_subscription
    )


class TriggerEventPayload(BaseModel):
    event: EventType
    context: EventContext
    web_push_subscription: dict[str, Any] | None = None


@router.post("/triggers/event")
async def trigger_event(
    payload: TriggerEventPayload,
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    trigger_ctrl = TriggerController(db)
    events_results = await trigger_ctrl.trigger_event(
        event=payload.event,
        context=payload.context,
        web_push_subscription=payload.web_push_subscription,
    )
    return events_results
