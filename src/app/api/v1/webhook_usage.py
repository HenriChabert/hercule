from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.api.dependencies import get_current_user

from src.app.controllers.webhook_usage import WebhookUsageController
from src.app.core.config import Settings
from src.app.core.db.database import async_get_db
from src.app.schemas.webhook_usage import WebhookUsage as WebhookUsageSchema
from src.app.schemas.webhook_usage import WebhookUsageCallbackPayload
from src.app.schemas.user import User as UserSchema

settings = Settings()
router = APIRouter(tags=["webhook_usage"], dependencies=[Depends(get_current_user)])


@router.get("/webhook-usage/{webhook_usage_id}")
async def get_webhook_usage(
    webhook_usage_id: str,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> WebhookUsageSchema:
    webhook_usage_ctrl = WebhookUsageController(db)
    return await webhook_usage_ctrl.read_safe(webhook_usage_id)


@router.post("/webhook-usage/{webhook_usage_id}/callback")
async def webhook_usage_callback(
    webhook_usage_id: str,
    payload: WebhookUsageCallbackPayload,
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    webhook_usage_ctrl = WebhookUsageController(db)
    success = await webhook_usage_ctrl.callback(webhook_usage_id, payload)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to callback webhook usage")
    return JSONResponse(
        status_code=200, content={"message": "Webhook usage callback successful"}
    )
