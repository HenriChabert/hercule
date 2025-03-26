from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.dependencies import get_current_admin_user, get_current_user
from src.app.controllers.webhook import WebhookController
from src.app.core.db.database import async_get_db
from src.app.schemas.user import User as UserSchema
from src.app.schemas.webhook import WebhookCreate, WebhookUpdate

router = APIRouter(tags=["webhook"], dependencies=[Depends(get_current_user)])


@router.post("/webhook", status_code=status.HTTP_201_CREATED)
async def create_webhook(
    webhook: WebhookCreate,
    current_user: Annotated[UserSchema, Depends(get_current_admin_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    webhook_ctrl = WebhookController(db)
    return await webhook_ctrl.create(webhook)


@router.get("/webhook/{webhook_id}")
async def get_webhook(
    webhook_id: str,
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    webhook_ctrl = WebhookController(db)
    return await webhook_ctrl.read(webhook_id, allow_none=False)


@router.get("/webhooks")
async def get_webhooks(
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    webhook_ctrl = WebhookController(db)
    return await webhook_ctrl.list()


@router.put("/webhook/{webhook_id}")
async def update_webhook(
    webhook_id: str,
    webhook: WebhookUpdate,
    current_user: Annotated[UserSchema, Depends(get_current_admin_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    webhook_ctrl = WebhookController(db)
    return await webhook_ctrl.update(webhook_id, webhook)


@router.delete("/webhook/{webhook_id}")
async def delete_webhook(
    webhook_id: str,
    current_user: Annotated[UserSchema, Depends(get_current_admin_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    webhook_ctrl = WebhookController(db)
    return await webhook_ctrl.delete(webhook_id)
