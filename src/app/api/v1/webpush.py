from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.app.core.config import Settings

settings = Settings()
router = APIRouter(tags=["webpush"])

@router.get("/webpush/public-key")
async def get_public_key():
    return JSONResponse(content={
        "public_key": settings.APP_SERVER_KEY
    })
