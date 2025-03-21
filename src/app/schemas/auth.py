from pydantic import BaseModel, EmailStr

from src.app.schemas.user import User, UserUnsafe

class AuthBase(BaseModel):
    email: EmailStr
    password: str

class AuthLogin(AuthBase):
    pass

class AuthLoginResponse(BaseModel):
    user: UserUnsafe
    token: 'Token'

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: str | None = None 