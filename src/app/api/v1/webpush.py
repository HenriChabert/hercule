from typing import Any, Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from webpush import WebPushSubscription  # type: ignore

from src.app.api.dependencies import get_current_user
from src.app.schemas.user import User as UserSchema
from src.app.core.config import Settings
from src.app.helpers.webpush import send_webpush as send_webpush_helper

settings = Settings()
router = APIRouter(tags=["webpush"], dependencies=[Depends(get_current_user)])


@router.get("/webpush/public-key")
async def get_public_key():
    return JSONResponse(content={"public_key": settings.APP_SERVER_KEY})


class SendWebpushBody(BaseModel):
    subscription: WebPushSubscription
    payload: dict[str, Any]


@router.post("/webpush/send")
async def send_webpush(
    payload: SendWebpushBody,
):
    success = await send_webpush_helper(
        payload.subscription.model_dump(), payload.payload
    )
    return JSONResponse(content={"success": success})
