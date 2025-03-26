import pytest
from fastapi.testclient import TestClient
from playwright.async_api import Page
from webpush import WebPushSubscription  # type: ignore

from src.app.core.config import settings


def test_get_public_key(client_auth: TestClient):
    response = client_auth.get("/api/v1/webpush/public-key")
    assert response.status_code == 200

    assert response.json() == {"public_key": settings.APP_SERVER_KEY}


@pytest.mark.asyncio
async def test_web_push_notification(
    push_test_page: Page,
    push_subscription: WebPushSubscription,
    client_auth: TestClient,
):
    assert push_subscription is not None

    push_sub = push_subscription.model_dump()
    push_sub["endpoint"] = str(push_sub["endpoint"])

    console_logs: list[str] = []
    push_test_page.on("console", lambda msg: console_logs.append(msg.text))

    await push_test_page.wait_for_timeout(2000)

    response = client_auth.post(
        "/api/v1/webpush/send",
        json={"subscription": push_sub, "payload": {"message": "Test notification"}},
    )
    assert response.status_code == 200

    received = await push_test_page.wait_for_function(
        "window.pushReceived", timeout=2000
    )
    assert received

    assert len(console_logs) > 0
