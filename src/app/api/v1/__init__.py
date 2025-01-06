from fastapi import APIRouter

from .system import router as system_router
from .webhook import router as webhook_router
from .trigger import router as trigger_router
from .webpush import router as webpush_router

router = APIRouter(prefix="/v1")
router.include_router(system_router)
router.include_router(webhook_router)
router.include_router(trigger_router)
router.include_router(webpush_router)
