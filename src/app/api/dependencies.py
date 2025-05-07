from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.controllers.auth import AuthController
from src.app.core.config import settings
from src.app.core.db.database import async_get_db
from src.app.schemas.user import User as UserSchema

header_scheme = APIKeyHeader(name="X-Hercule-Secret-Key")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login", auto_error=False)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> UserSchema:
    auth_ctrl = AuthController(db)
    if not settings.AUTH_REQUIRED:
        return auth_ctrl.get_anon_user()

    return await auth_ctrl.get_current_user(token)


async def get_current_admin_user(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> UserSchema:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return current_user
