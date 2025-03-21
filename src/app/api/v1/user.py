from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.database import async_get_db
from src.app.core.security import create_access_token, verify_password
from src.app.controllers.user import UserController
from src.app.schemas.user import UserCreate, User as UserSchema

router = APIRouter(tags=["user"])

@router.get("/user/{user_id}", status_code=status.HTTP_201_CREATED)
async def get_user(
    user_id: str,
    db: Annotated[AsyncSession, Depends(async_get_db)]
) -> UserSchema:
    user_ctrl = UserController(db)
    return await user_ctrl.read_safe(user_id)
    