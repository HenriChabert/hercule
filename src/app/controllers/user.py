import logging
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.controllers.base import BaseController
from src.app.crud.user import UserCRUD
from src.app.models.user import User as UserModel
from src.app.schemas.user import User as UserSchema
from src.app.schemas.user import UserCreate

logger = logging.getLogger(__name__)


class UserController(BaseController[UserSchema, UserModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.crud = UserCRUD(db)

    def get_anon_user(self) -> UserSchema:
        return UserSchema(
            id="anonymous",
            email="anonymous@example.com",
            role="user",
            hashed_password="",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    async def read(self, user_id: str, allow_none: bool = False) -> UserSchema | None:
        return await self.crud.read(user_id, allow_none)

    async def read_safe(self, user_id: str) -> UserSchema:
        return await self.crud.read_safe(user_id)

    async def create(self, user_create: UserCreate) -> UserSchema:
        user_dto = UserCreate(**user_create.model_dump())
        return await self.crud.create(user_dto)

    async def get_by_email(self, email: str) -> UserSchema | None:
        return await self.crud.get_by_email(email)

    async def list(self) -> list[UserSchema]:
        return await self.crud.list()
