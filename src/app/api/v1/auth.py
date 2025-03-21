from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.database import async_get_db
from src.app.schemas.auth import Token, AuthLogin
from src.app.schemas.user import User as UserSchema
from src.app.controllers.auth import AuthController
from src.app.api.dependencies import get_current_user

router = APIRouter(tags=["auth"])

@router.post("/auth/login", response_model=Token)
async def login(
    login_data: AuthLogin,
    db: Annotated[AsyncSession, Depends(async_get_db)]
) -> Token:
    auth_ctrl = AuthController(db)
    return await auth_ctrl.login(login_data)

@router.get("/auth/me", response_model=UserSchema)
async def me(
    current_user: Annotated[UserSchema, Depends(get_current_user)]
) -> UserSchema:
    return current_user