from fastapi import APIRouter, status

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from typing import Annotated

from src.app.schemas.webhook import WebhookCreate, WebhookUpdate
from src.app.controllers.webhook import WebhookController
from src.app.core.db.database import async_get_db
from src.app.api.dependencies import check_secret_key_header

router = APIRouter(tags=["webhook"], dependencies=[Depends(check_secret_key_header)])

@router.post("/webhook", status_code=status.HTTP_201_CREATED)
async def create_webhook(webhook: WebhookCreate, db: Annotated[AsyncSession, Depends(async_get_db)]):
    webhook_ctrl = WebhookController(db)
    return await webhook_ctrl.create(webhook)

@router.get("/webhook/{webhook_id}")
async def get_webhook(webhook_id: str, db: Annotated[AsyncSession, Depends(async_get_db)]):
    webhook_ctrl = WebhookController(db)
    return await webhook_ctrl.read(webhook_id, raise_exception=True)

@router.get("/webhooks")
async def get_webhooks(db: Annotated[AsyncSession, Depends(async_get_db)]):
    webhook_ctrl = WebhookController(db)
    return await webhook_ctrl.list()    

@router.put("/webhook/{webhook_id}")
async def update_webhook(webhook_id: str, webhook: WebhookUpdate, db: Annotated[AsyncSession, Depends(async_get_db)]):
    webhook_ctrl = WebhookController(db)
    return await webhook_ctrl.update(webhook_id, webhook)

@router.delete("/webhook/{webhook_id}")
async def delete_webhook(webhook_id: str, db: Annotated[AsyncSession, Depends(async_get_db)]):
    webhook_ctrl = WebhookController(db)
    return await webhook_ctrl.delete(webhook_id)