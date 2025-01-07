import os

from dotenv import load_dotenv
from fastapi import FastAPI
from playwright.sync_api import BrowserContext
from webpush import WebPushSubscription  # type: ignore

current_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(f"{current_dir}/../.env.test", override=True)

from typing import Any, Callable, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import Session

from src.app.core.config import settings
from src.app.core.db.database import (
    async_get_db,
    clean_db,
    reinit_db,
    sync_engine,
    sync_get_db,
)

from .helpers.web_services.test_api.main import create_test_api
from .helpers.web_services.test_web_server.main import create_static_web_server
from .helpers.web_services.utils import (
    find_free_port,
    run_test_server,
    stop_test_server,
)


@pytest.fixture(autouse=True)
def reset_db_each_test():
    reinit_db()
    yield
    clean_db()

def test_server_url_fixture(create_fn: Callable[[], FastAPI]):
    host = "127.0.0.1"
    port = find_free_port()

    server_thread = run_test_server(create_fn(), host, port)

    base_url = f"http://{host}:{port}"
    yield base_url

    stop_test_server(server_thread)


@pytest.fixture(scope="session")
def test_api_url() -> Generator[str, Any, None]:
    yield from test_server_url_fixture(create_test_api)

@pytest.fixture(scope="session")
def test_web_server_url() -> Generator[str, Any, None]:
    yield from test_server_url_fixture(create_static_web_server)


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, Any, None]:
    from src.app.main import app

    with TestClient(app) as _client:
        _client.headers[settings.HERCULE_HEADER_NAME] = os.getenv(
            "HERCULE_SECRET_KEY", ""
        )
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


@pytest_asyncio.fixture(scope="function")  # type: ignore
async def db() -> AsyncSession:
    session_gen = async_get_db()
    session = await anext(session_gen)
    return session


from playwright.sync_api import Browser, Page, sync_playwright


@pytest.fixture(scope="session")
def browser_context() -> Generator[BrowserContext, Any, None]:
    with sync_playwright() as p:
        # browser = p.chromium.connect_over_cdp(
        #     f"ws://127.0.0.1:9222/devtools/browser/68117ca3-64a8-489e-b12f-86196dc47e7b"
        # )
        # context = browser.contexts[0]
        context = p.chromium.launch_persistent_context(
            headless=True,
            user_data_dir=f"/tmp/tests/playwright",
            permissions=["notifications"],
            channel="chromium",
            args=[
                "--enable-features=NetworkService,NetworkServiceInProcess --allow-silent-push --enable-logging=stderr"
            ],
            service_workers="allow"
        )

        yield context
        context.close()

@pytest.fixture
def push_test_page(test_web_server_url: str, browser_context: BrowserContext):
    page = browser_context.new_page()
    page.on("console", lambda msg: print("Console:", msg.text))

    page.goto(f"{test_web_server_url}/test-push.html")

    page.wait_for_function("window.serviceWorkerActivated", timeout=1000)

    yield page

    page.close()

@pytest.fixture
def push_subscription(push_test_page: Page):
    # Wait for subscription with a timeout
    subscription = WebPushSubscription.model_validate(
        push_test_page.evaluate(
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
        }""" % settings.APP_SERVER_KEY)
    )

    yield subscription