import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.security import create_access_token
from tests.helpers.fakers.user import UserFaker
from src.app.core.config import settings
from src.app.models.user import User

pytestmark = pytest.mark.asyncio

user_faker = UserFaker()


@pytest.mark.asyncio
async def test_auth_login(client_anon: TestClient, db: AsyncSession):
    password = "password"
    user = await user_faker.create_fake(db, {"password": password})
    response = client_anon.post(
        "/api/v1/auth/login", json={"email": user.email, "password": password}
    )
    assert response.status_code == 200
    assert response.json()["token"]["access_token"] is not None


@pytest.mark.asyncio
async def test_auth_login_invalid_password(client_anon: TestClient, db: AsyncSession):
    password = "password"
    user = await user_faker.create_fake(db, {"password": password})
    response = client_anon.post(
        "/api/v1/auth/login", json={"email": user.email, "password": "invalid"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_auth_not_required(client_anon: TestClient, db: AsyncSession):
    settings.AUTH_REQUIRED = False
    response = client_anon.get("/api/v1/auth/me")
    assert response.status_code == 200
    assert response.json()["email"] == "anonymous@example.com"
    settings.AUTH_REQUIRED = True


@pytest.mark.asyncio
async def test_auth_me(client_auth: TestClient, db: AsyncSession, test_user: User):
    response = client_auth.get("/api/v1/auth/me")

    assert response.status_code == 200
    assert response.json()["email"] == test_user.email


@pytest.mark.asyncio
async def test_auth_me_invalid_token(client_anon: TestClient, db: AsyncSession):
    response = client_anon.get(
        "/api/v1/auth/me", headers={"Authorization": "Bearer invalid"}
    )
    assert response.status_code == 401
