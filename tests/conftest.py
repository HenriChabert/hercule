import os
from contextlib import ExitStack

from dotenv import load_dotenv
from fastapi import FastAPI
from playwright.async_api import Browser, BrowserContext, Page, async_playwright
from webpush import WebPushSubscription  # type: ignore

current_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(f"{current_dir}/../.env.test", override=True)

from typing import Any, AsyncGenerator, Callable, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import Session

from src.app.core.config import settings
from src.app.core.db.database import async_get_db, session_manager
from src.app.core.setup import init_app

from .helpers.web_services.test_api.main import create_test_api
from .helpers.web_services.test_web_server.main import create_static_web_server
from .helpers.web_services.utils import (
    find_free_port,
    run_test_server,
    stop_test_server,
)


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield init_app(init_db=False)

@pytest.fixture
def client(app: FastAPI) -> Generator[TestClient, Any, None]:
    with TestClient(app) as c:
        c.headers[settings.HERCULE_HEADER_NAME] = os.getenv(
            "HERCULE_SECRET_KEY", ""
        )
        yield c

@pytest_asyncio.fixture(scope="session", autouse=True)  # type: ignore
async def connection_test():
    host = settings.SQLITE_URI
    session_manager.init(host)
    yield
    await session_manager.close()

@pytest_asyncio.fixture(scope="function", autouse=True)  # type: ignore
async def create_tables(db: AsyncSession):
    async with session_manager.connect() as connection:
        await session_manager.drop_all(connection)
        await session_manager.create_all(connection)

@pytest_asyncio.fixture(scope="function", autouse=True)  # type: ignore
async def session_override(app: FastAPI, db: AsyncSession):
    async def get_db_override():
        async with session_manager.session() as session:
            yield session

    app.dependency_overrides[async_get_db] = get_db_override

@pytest_asyncio.fixture  # type: ignore
async def db() -> AsyncGenerator[AsyncSession, Any]:
    async with session_manager.session() as session:
        yield session


def test_server_url_fixture(create_fn: Callable[[], FastAPI]):
    host = "127.0.0.1"
    port = find_free_port()

    fastapi_app = create_fn()

    print(f"Starting server on {host}:{port}")
    server_process = run_test_server(fastapi_app, host, port)

    base_url = f"http://{host}:{port}"
    yield base_url

    stop_test_server(server_process)


@pytest.fixture(scope="session")
def test_api_url() -> Generator[str, Any, None]:
    yield from test_server_url_fixture(create_test_api)


@pytest.fixture(scope="session")
def test_web_server_url() -> Generator[str, Any, None]:
    yield from test_server_url_fixture(create_static_web_server)


@pytest.fixture
def client_no_key(client: TestClient) -> Generator[TestClient, Any, None]:
    prev_header = client.headers.get(settings.HERCULE_HEADER_NAME)
    if prev_header:
        del client.headers[settings.HERCULE_HEADER_NAME]
    yield client
    if prev_header:
        client.headers[settings.HERCULE_HEADER_NAME] = prev_header


@pytest_asyncio.fixture # type: ignore
async def browser_context() -> AsyncGenerator[BrowserContext, Any]:

    async with async_playwright() as p:
        # browser = p.chromium.connect_over_cdp(
        #     f"ws://127.0.0.1:9222/devtools/browser/68117ca3-64a8-489e-b12f-86196dc47e7b"
        # )
        # context = browser.contexts[0]
        context = await p.chromium.launch_persistent_context(
            headless=True,
            user_data_dir=f"/tmp/tests/playwright",
            permissions=["notifications"],
            channel="chromium",
            args=[
                "--enable-features=NetworkService,NetworkServiceInProcess --allow-silent-push --enable-logging=stderr"
            ],
            service_workers="allow",
        )

        yield context
        await context.close()


@pytest_asyncio.fixture # type: ignore
async def push_test_page(test_web_server_url: str, browser_context: BrowserContext):
    page = await browser_context.new_page()
    page.on("console", lambda msg: print("Console:", msg.text))

    await page.goto(f"{test_web_server_url}/test-push.html")

    await page.wait_for_function("window.serviceWorkerActivated", timeout=1000)

    yield page

    await page.close()


@pytest_asyncio.fixture # type: ignore
async def push_subscription(push_test_page: Page):
    # Wait for subscription with a timeout
    evaluate_result = await push_test_page.evaluate(
            """() => {
            return new Promise((resolve, reject) => {
                const timeout = setTimeout(() => {
                    reject(new Error('Subscription timed out'));
                }, 5000);  // 5 second timeout

                navigator.serviceWorker.ready.then((registration) => {
                    registration.pushManager.subscribe({
                        userVisibleOnly: true,
                        applicationServerKey: '%s'
                    })
                    .then((subscription) => {
                        clearTimeout(timeout);
                        console.log("Subscription:", subscription.toJSON());
                        resolve(subscription.toJSON());
                    })
                    .catch((error) => {
                        clearTimeout(timeout);
                        reject(error);
                    });
                });
            });
        }"""
            % settings.APP_SERVER_KEY
        )
        
    subscription = WebPushSubscription.model_validate(
        evaluate_result
    )

    yield subscription
