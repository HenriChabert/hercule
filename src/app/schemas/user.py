from pydantic import BaseModel, EmailStr

from src.app.core.schemas import IDSchema, TimestampSchema
from src.app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    role: UserRole
    hashed_password: str


class User(UserBase, IDSchema, TimestampSchema):
    pass


class UserUnsafe(BaseModel):
    role: UserRole
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str | None = None


class UserUpdateHashedPassword(UserBase):
    hashed_password: str


class UserLogin(UserBase):
    password: str
