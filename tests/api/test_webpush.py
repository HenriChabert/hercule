from fastapi.testclient import TestClient
from playwright.sync_api import Page
from webpush import WebPushSubscription  # type: ignore

from src.app.core.config import settings


def test_get_public_key(client: TestClient):
    response = client.get("/api/v1/webpush/public-key")
    assert response.status_code == 200

    assert response.json() == {"public_key": settings.APP_SERVER_KEY}


def test_web_push_notification(
    push_test_page: Page, push_subscription: WebPushSubscription, client: TestClient
):
    assert push_subscription is not None

    push_sub = push_subscription.model_dump()
    push_sub["endpoint"] = str(push_sub["endpoint"])

    console_logs: list[str] = []
    push_test_page.on("console", lambda msg: console_logs.append(msg.text))

    response = client.post(
        "/api/v1/webpush/send",
        json={"subscription": push_sub, "payload": {"message": "Test notification"}},
    )
    assert response.status_code == 200

    received = push_test_page.wait_for_function("window.pushReceived", timeout=1000)
    assert received

    assert len(console_logs) > 0
