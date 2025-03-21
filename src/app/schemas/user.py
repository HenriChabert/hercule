from pydantic import BaseModel, EmailStr

from ..core.schemas import IDSchema, TimestampSchema

class UserBase(BaseModel):
    email: EmailStr
    hashed_password: str

class User(UserBase, IDSchema, TimestampSchema):
    pass

class UserUnsafe(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: str | None = None

class UserUpdateHashedPassword(UserBase):
    hashed_password: str

class UserLogin(UserBase):
    password: str