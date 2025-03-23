import datetime
from typing import NotRequired, TypedDict
import random as rd

from src.app import models
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseFaker
from src.app.core.security import get_password_hash
from src.app.models.user import UserRole


class UserFields(TypedDict):
    id: NotRequired[str]
    email: NotRequired[str]
    role: NotRequired[UserRole]
    password: NotRequired[str]
    is_active: NotRequired[bool]
    created_at: NotRequired[datetime.datetime]
    updated_at: NotRequired[datetime.datetime]


class UserFaker(BaseFaker[models.User]):
    def get_fake(self, fields: UserFields | None = None) -> models.User:
        if fields is None:
            fields = UserFields()

        hashed_password = fields.get("hashed_password", get_password_hash(fields.get("password", self.fake.password(length=12))))

        return models.User(
            id=fields.get("id", str(self.fake.uuid4())),
            email=fields.get("email", self.fake.email()),
            role=fields.get("role", rd.choice(["user", "admin"])),
            hashed_password=hashed_password,  # bcrypt hash length
            is_active=fields.get("is_active", True),
            created_at=fields.get("created_at", datetime.datetime.now()),
            updated_at=fields.get("updated_at", datetime.datetime.now())
        )

    async def create_fake(self, db: AsyncSession, fields: UserFields | None = None) -> models.User:
        new_user = await self.create_fake_object(db, self.get_fake, fields)
        return new_user