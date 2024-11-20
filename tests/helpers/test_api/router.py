from fastapi import APIRouter
from typing import Any, Mapping

router = APIRouter(tags=["test"])

@router.post("/test_webhook")
async def test_webhook(payload: Mapping[str, Any]):
    return {"status": "ok"}