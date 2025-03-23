from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.database import async_get_db
from src.app.controllers.user import UserController
from src.app.schemas.user import User as UserSchema
from src.app.api.dependencies import get_current_admin_user

router = APIRouter(tags=["user"], dependencies=[Depends(get_current_admin_user)])


@router.get("/user/{user_id}", status_code=status.HTTP_201_CREATED)
async def get_user(
    user_id: str, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> UserSchema:
    user_ctrl = UserController(db)
    return await user_ctrl.read_safe(user_id)


@router.get("/users", status_code=status.HTTP_201_CREATED)
async def get_users(
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> list[UserSchema]:
    user_ctrl = UserController(db)
    return await user_ctrl.list()
