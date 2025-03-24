from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.controllers.user import UserController
from src.app.core.security import (create_access_token, verify_password,
                                   verify_token)
from src.app.schemas.auth import AuthLogin, AuthLoginResponse, Token
from src.app.schemas.user import User as UserSchema
from src.app.schemas.user import UserUnsafe


class AuthController:
    def __init__(self, db: AsyncSession):
        self.db = db

    def get_anon_user(self) -> UserSchema:
        user_ctrl = UserController(self.db)
        return user_ctrl.get_anon_user()

    async def login(self, auth_login: AuthLogin) -> AuthLoginResponse:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        user_ctrl = UserController(self.db)
        user = await user_ctrl.get_by_email(auth_login.email)
        if not user:
            raise credentials_exception

        if not verify_password(auth_login.password, user.hashed_password):
            raise credentials_exception

        access_token = create_access_token(data={"sub": user.email})
        user_unsafe = UserUnsafe(
            email=user.email,
            role=user.role,
        )
        return AuthLoginResponse(
            user=user_unsafe, token=Token(access_token=access_token)
        )

    async def logout(self, token: str) -> None:
        pass

    async def get_me(self, user: UserSchema) -> UserUnsafe:
        return UserUnsafe(
            email=user.email,
            role=user.role,
        )

    async def get_current_user(self, token: str) -> UserSchema:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        if not token:
            raise credentials_exception

        email = verify_token(token)
        if not email:
            raise credentials_exception
        user_ctrl = UserController(self.db)

        user = await user_ctrl.get_by_email(email)
        if not user:
            raise credentials_exception
        return user
