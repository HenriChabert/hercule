from pydantic import BaseModel, EmailStr

from ..core.schemas import IDSchema, TimestampSchema

class AuthBase(BaseModel):
    email: EmailStr
    password: str

class AuthLogin(AuthBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: str | None = None 