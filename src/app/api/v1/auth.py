from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.dependencies import get_current_user, oauth2_scheme
from src.app.controllers.auth import AuthController
from src.app.core.db.database import async_get_db
from src.app.schemas.auth import AuthLogin, AuthLoginResponse, UserUnsafe
from src.app.schemas.user import User as UserSchema

router = APIRouter(tags=["auth"])


@router.post("/auth/login", response_model=AuthLoginResponse)
async def login(
    login_data: AuthLogin, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> AuthLoginResponse:
    auth_ctrl = AuthController(db)
    login_response = await auth_ctrl.login(login_data)
    return login_response


@router.post("/auth/logout")
async def logout(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    auth_ctrl = AuthController(db)
    await auth_ctrl.logout(token)
    return JSONResponse(status_code=201, content={"message": "Successfully logged out"})


@router.get("/auth/me", response_model=UserUnsafe)
async def me(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> UserUnsafe:
    auth_ctrl = AuthController(db)
    return await auth_ctrl.get_me(current_user)
