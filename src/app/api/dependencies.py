from fastapi import Depends, Security, HTTPException, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.security import check_secret_key
from src.app.controllers.auth import AuthController
from src.app.core.db.database import async_get_db
from src.app.schemas.user import User as UserSchema
from src.app.core.config import settings

header_scheme = APIKeyHeader(name="X-Hercule-Secret-Key")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login", auto_error=False)

def is_user_admin(secret_key: str = Depends(header_scheme)):
    if not check_secret_key(secret_key):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="This resource is only available to admins")
    return True

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(async_get_db)]
) -> UserSchema:
    auth_ctrl = AuthController(db)
    if not settings.AUTH_REQUIRED:
        return auth_ctrl.get_anon_user()
    
    return await auth_ctrl.get_current_user(token)