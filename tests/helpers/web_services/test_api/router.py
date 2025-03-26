from typing import Any, Mapping

from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["test"])


@router.post("/test_webhook")
async def test_webhook(payload: Mapping[str, Any]):
    return {"status": "success"}


@router.post("/test_webhook_error")
async def test_webhook_error(payload: Mapping[str, Any]):
    raise HTTPException(status_code=500, detail="Test Error")


@router.post("/test_show_console_action")
async def test_show_console_action(payload: Mapping[str, Any]):
    return {
        "status": "success",
        "actions": [{"type": "show_console", "params": {"message": "Test Works"}}],
    }
