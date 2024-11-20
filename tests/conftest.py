
import os

os.environ["TESTING"] = "true"
os.environ["CONFIG_DIR"] = "/tmp/tests"
os.environ["SQLITE_DB_NAME"] = "test.db"

from typing import Any, Generator

import pytest
import pytest_asyncio
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.database import Base, reinit_db, clean_db, async_get_db, sync_get_db, async_engine, sync_engine

@pytest.fixture(autouse=True)
def reset_db_each_test():
    reinit_db()
    yield
    clean_db()

@pytest.fixture(scope="session")
def client() -> Generator[TestClient, Any, None]:
    from src.app.main import app

    with TestClient(app) as _client:
        yield _client
    app.dependency_overrides = {}
    sync_engine.dispose()


@pytest.fixture
def db_sync() -> Generator[Session, Any, None]:
    session = sync_get_db()
    yield session
    session.close()

@pytest_asyncio.fixture # type: ignore
async def db() -> AsyncSession:
    session_gen = async_get_db()
    session = await anext(session_gen)
    return session
