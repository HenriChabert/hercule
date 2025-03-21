import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.security import create_access_token
from tests.helpers.fakers.user import UserFaker
from src.app.core.config import settings

pytestmark = pytest.mark.asyncio

user_faker = UserFaker()


@pytest.mark.asyncio
async def test_auth_login(client: TestClient, db: AsyncSession):
    password = "password"
    user = await user_faker.create_fake(db, {"password": password})
    response = client.post(
        "/api/v1/auth/login", json={"email": user.email, "password": password}
    )
    assert response.status_code == 200
    assert response.json()["access_token"] is not None

@pytest.mark.asyncio
async def test_auth_login_invalid_password(client: TestClient, db: AsyncSession):
    password = "password"
    user = await user_faker.create_fake(db, {"password": password})
    response = client.post("/api/v1/auth/login", json={"email": user.email, "password": "invalid"})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_auth_not_required(client: TestClient, db: AsyncSession):
    settings.AUTH_REQUIRED = False
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 200
    assert response.json()["email"] == "anonymous@example.com"
    settings.AUTH_REQUIRED = True


@pytest.mark.asyncio
async def test_auth_me(client: TestClient, db: AsyncSession):
    password = "password"
    user = await user_faker.create_fake(db, {"password": password})
    access_token = create_access_token({"sub": user.email})

    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    assert response.json()["email"] == user.email

@pytest.mark.asyncio
async def test_auth_me_invalid_token(client: TestClient, db: AsyncSession):
    response = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid"})
    assert response.status_code == 401


