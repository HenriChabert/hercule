from fastapi import APIRouter
from typing import Any, Mapping

router = APIRouter(tags=["test"])

@router.post("/test_webhook")
async def test_webhook(payload: Mapping[str, Any]):
    return {"status": "success"}

@router.post("/test_show_console_action")
async def test_show_console_action(payload: Mapping[str, Any]):
    return {
        "status": "success",
        "actions": [
            {
                "type": "show_console",
                "params": {
                    "message": "Test Works"
                }
            }
        ]
    }
