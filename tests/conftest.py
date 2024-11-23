import os

from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(f"{current_dir}/../.env.test", override=True)

from typing import Any, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.database import reinit_db, clean_db, async_get_db, sync_get_db, sync_engine
from .helpers.test_api.main import create_test_client, run_test_server, find_free_port, stop_test_server

from src.app.core.config import settings

@pytest.fixture(autouse=True)
def reset_db_each_test():
    reinit_db()
    yield
    clean_db()

@pytest.fixture(scope="session")
def test_api_url():
    # Define a new FastAPI app specifically for testing
    app = create_test_client()

    host = "127.0.0.1"
    port = find_free_port()

    # Run the test server
    server_thread = run_test_server(app, host, port)

    # Yield the base URL for the test server
    base_url = f"http://{host}:{port}"
    yield base_url

    # Stop the server after tests
    stop_test_server(server_thread)


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, Any, None]:
    from src.app.main import app
    from tests.helpers.test_api.router import router as test_router

    app.include_router(test_router)

    with TestClient(app) as _client:
        _client.headers[settings.HERCULE_HEADER_NAME] = os.getenv("HERCULE_SECRET_KEY", "")
        yield _client
    app.dependency_overrides = {}
    sync_engine.dispose()

@pytest.fixture
def client_no_key(client: TestClient) -> Generator[TestClient, Any, None]:
    prev_header = client.headers.get(settings.HERCULE_HEADER_NAME)
    if prev_header:
        del client.headers[settings.HERCULE_HEADER_NAME]
    yield client
    if prev_header:
        client.headers[settings.HERCULE_HEADER_NAME] = prev_header

@pytest.fixture
def db_sync() -> Generator[Session, Any, None]:
    session = sync_get_db()
    yield session
    session.close()

@pytest_asyncio.fixture(scope="function") # type: ignore
async def db() -> AsyncSession:
    session_gen = async_get_db()
    session = await anext(session_gen)
    return session
