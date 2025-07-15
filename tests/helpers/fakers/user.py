import datetime
import random as rd

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.app import models
from src.app.core.security import get_password_hash
from src.app.models.user import UserRole

from .base import BaseFaker


class UserFields(BaseModel):
    id: str | None = None
    email: str | None = None
    role: UserRole | None = None
    hashed_password: str | None = None
    password: str | None = None
    is_active: bool | None = None
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None


class UserFaker(BaseFaker[models.User]):
    def get_fake(self, fields: UserFields | None = None) -> models.User:
        if fields is None:
            fields = UserFields()

        hashed_password = fields.hashed_password or get_password_hash(
            fields.password or self.fake.password(length=12),
        )

        return models.User(
            id=fields.id or str(self.fake.uuid4()),
            email=fields.email or self.fake.email(),
            role=fields.role or rd.choice(["user", "admin"]),
            hashed_password=hashed_password,  # bcrypt hash length
            is_active=fields.is_active or True,
            created_at=fields.created_at or datetime.datetime.now(),
            updated_at=fields.updated_at or datetime.datetime.now(),
        )

    async def create_fake(
        self, db: AsyncSession, fields: UserFields | None = None
    ) -> models.User:
        new_user = await self.create_fake_object(db, self.get_fake, fields)
        return new_user
