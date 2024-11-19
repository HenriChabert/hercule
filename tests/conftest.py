from typing import Any, Callable, Generator

import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from src.app.core.config import settings
from src.app.main import app
from src.app.core.db.database import Base
DATABASE_URI = settings.SQLITE_URI_TEST
DATABASE_PREFIX = settings.SQLITE_SYNC_PREFIX

sync_engine = create_engine(DATABASE_PREFIX + DATABASE_URI)
local_session = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


fake = Faker()

def reset_db():
    Base.metadata.drop_all(bind=sync_engine)
    Base.metadata.create_all(bind=sync_engine)


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, Any, None]:
    with TestClient(app) as _client:
        yield _client
    app.dependency_overrides = {}
    sync_engine.dispose()


@pytest.fixture
def db() -> Generator[Session, Any, None]:
    session = local_session()
    yield session
    session.close()


def override_dependency(dependency: Callable[..., Any], mocked_response: Any) -> None:
    app.dependency_overrides[dependency] = lambda: mocked_response
