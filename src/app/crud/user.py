from typing import Any, cast

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User as UserModel
from ..schemas.user import User as UserSchema, UserUpdateHashedPassword
from ..schemas.user import UserCreate
from ..types.events import EventType
from .base import BaseCRUD


class UserCRUD(BaseCRUD[UserSchema, UserModel]):
    def model_to_schema(self, model: UserModel) -> UserSchema:
        model_dump = {
            "id": model.id,
            "email": model.email,
            "role": model.role,
            "hashed_password": model.hashed_password,
            "is_active": model.is_active,
            "created_at": model.created_at,
            "updated_at": model.updated_at,
        }
        return UserSchema.model_validate(model_dump)

    async def _read_orm(self, id: str, allow_none: bool = True) -> UserModel | None:
        query = select(UserModel).where(UserModel.id == id)

        result = await self.db.execute(query)

        user = result.scalar_one_or_none()
        if not user and not allow_none:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    
    async def get_by_email(self, email: str) -> UserSchema | None:
        query = select(UserModel).where(UserModel.email == email)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return self.model_to_schema(user)
    
    async def list(self, **kwargs: Any) -> list[UserSchema]:
        query = select(UserModel)
        result = await self.db.execute(query)
        return [self.model_to_schema(user) for user in result.scalars().all()]
    
    async def create(self, data: UserCreate) -> UserSchema:
        user = UserModel(**data.model_dump())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return self.model_to_schema(user)
    
    async def update(self, id: str, data: UserUpdateHashedPassword) -> UserSchema:
        user = await self._read_orm_safe(id)
        user = self.update_object(user, data)
        await self.db.commit()
        await self.db.refresh(user)
        return self.model_to_schema(user)
    
    async def delete(self, id: str) -> None:
        user = await self._read_orm_safe(id)
        await self.db.delete(user)
        await self.db.commit()
    
    