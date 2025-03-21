from fastapi import Request
from datetime import datetime, timedelta
from typing import Any

from jwt import encode as jwt_encode, decode as jwt_decode, PyJWTError
from passlib.context import CryptContext
from pydantic import EmailStr

from src.app.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt_encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> EmailStr | None:
    try:
        payload = jwt_decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            return None
        return email
    except PyJWTError:
        return None

def check_secret_key(secret_key: str) -> bool:
    return secret_key == settings.HERCULE_SECRET_KEY

def check_request_secret_key(request: Request) -> bool:
    secret_key = request.headers.get("X-Hercule-Secret-Key")
    if secret_key is None:
        return False
    return check_secret_key(secret_key)
