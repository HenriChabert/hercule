from typing import Any, Generator

import pytest
import pytest_asyncio
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from src.app.core.config import settings
from src.app.core.db.database import reset_db, async_get_db

DATABASE_URI = settings.SQLITE_URI_TEST
DATABASE_PREFIX = settings.SQLITE_SYNC_PREFIX

sync_engine = create_engine(DATABASE_PREFIX + DATABASE_URI)
local_session = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

fake = Faker()

@pytest.fixture(scope="session")
def client() -> Generator[TestClient, Any, None]:
    from src.app.main import app

    with TestClient(app) as _client:
        yield _client
    app.dependency_overrides = {}
    sync_engine.dispose()
    

@pytest_asyncio.fixture
async def db() -> AsyncSession:
    session_gen = async_get_db()
    session = await anext(session_gen)
    await reset_db()
    return session
