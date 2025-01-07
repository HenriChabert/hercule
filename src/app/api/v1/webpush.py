from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from webpush import WebPushSubscription  # type: ignore

from src.app.core.config import Settings
from src.app.helpers.webpush import send_webpush as send_webpush_helper

settings = Settings()
router = APIRouter(tags=["webpush"])

@router.get("/webpush/public-key")
async def get_public_key():
    return JSONResponse(content={
        "public_key": settings.APP_SERVER_KEY
    })

class SendWebpushBody(BaseModel):
    subscription: WebPushSubscription
    payload: dict[str, Any]

@router.post("/webpush/send")
async def send_webpush(payload: SendWebpushBody):
    success = await send_webpush_helper(payload.subscription.model_dump(), payload.payload)
    return JSONResponse(content={"success": success})
