from fastapi import APIRouter, Depends

from src.app.api.dependencies import get_current_user

router = APIRouter(tags=["system"])

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.get("/health-secured", dependencies=[Depends(get_current_user)])
async def ping_secured():
    return {"status": "ok"}

@router.get("/version")
async def version():
    return {"version": "0.1.0"}
