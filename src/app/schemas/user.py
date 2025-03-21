from pydantic import BaseModel, EmailStr

from ..core.schemas import IDSchema, TimestampSchema

class UserBase(BaseModel):
    email: EmailStr
    hashed_password: str

class UserUnsafeBase(UserBase):
    email: EmailStr

class User(UserBase, IDSchema, TimestampSchema):
    pass

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: str | None = None

class UserUpdateHashedPassword(UserBase):
    hashed_password: str

class UserLogin(UserBase):
    password: str