from fastapi import APIRouter

from ..api.v1 import router as v1_router

router = APIRouter(prefix="/api")