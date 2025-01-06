from fastapi import APIRouter

from src.app.core.config import Settings

settings = Settings()
router = APIRouter(tags=["webpush"])

@router.get("/webpush/public-key")
async def get_public_key():
    return settings.APP_SERVER_KEY