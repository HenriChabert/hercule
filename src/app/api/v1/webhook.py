from fastapi import APIRouter, Request, status

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from typing import Annotated

from src.app.schemas.webhook import WebhookCreate, WebhookUpdate, WebhookDelete
from src.app.crud.webhook import WebhookCRUD
from src.app.core.db.database import async_get_db

router = APIRouter(tags=["webhook"])

@router.post("/webhook", status_code=status.HTTP_201_CREATED)
async def create_webhook(webhook: WebhookCreate, db: Annotated[AsyncSession, Depends(async_get_db)]):
    webhook_crud = WebhookCRUD(db)
    return await webhook_crud.create(webhook)

@router.get("/webhook/{webhook_id}")
async def get_webhook(webhook_id: str, db: Annotated[AsyncSession, Depends(async_get_db)]):
    webhook_crud = WebhookCRUD(db)
    webhook = await webhook_crud.read(webhook_id)
    return webhook

@router.get("/webhooks")
async def get_webhooks(db: Annotated[AsyncSession, Depends(async_get_db)]):
    webhook_crud = WebhookCRUD(db)
    return await webhook_crud.list()    

@router.put("/webhook/{webhook_id}")
async def update_webhook(webhook_id: str, webhook: WebhookUpdate, db: Annotated[AsyncSession, Depends(async_get_db)]):
    webhook_crud = WebhookCRUD(db)
    return await webhook_crud.update(webhook_id, webhook)

@router.delete("/webhook/{webhook_id}")
async def delete_webhook(webhook_id: str, db: Annotated[AsyncSession, Depends(async_get_db)]):
    webhook_crud = WebhookCRUD(db)
    return await webhook_crud.delete(webhook_id)
