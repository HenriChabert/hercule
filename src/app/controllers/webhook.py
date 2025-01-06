import datetime
import hashlib
import hmac
import json
from typing import Any, Literal, Mapping, TypedDict, cast, overload

import httpx
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.controllers.base import BaseController
from src.app.controllers.webhook_usage import WebhookUsageController
from src.app.crud.webhook import WebhookCRUD
from src.app.models.webhook import Webhook as WebhookModel
from src.app.schemas.webhook import Webhook as WebhookSchema
from src.app.schemas.webhook import WebhookCreate, WebhookUpdate
from src.app.schemas.webhook_usage import WebhookUsageCreate
from src.app.types.actions import Action
from src.app.types.events import EventType


class WebhookCallResult(TypedDict):
    status: int
    actions: list[Action]


class WebhookController(BaseController[WebhookSchema, WebhookModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.crud = WebhookCRUD(db)
        self.webhook_usage_ctrl = WebhookUsageController(db)

    async def create(self, webhook: WebhookCreate) -> WebhookSchema:
        return await self.crud.create(webhook)

    @overload
    async def read(
        self, webhook_id: str, raise_exception: Literal[False] = False
    ) -> WebhookSchema | None: ...

    @overload
    async def read(
        self, webhook_id: str, raise_exception: Literal[True]
    ) -> WebhookSchema: ...

    async def read(
        self, webhook_id: str, raise_exception: bool = False
    ) -> WebhookSchema | None:
        webhook = await self.crud.read(webhook_id, allow_none=(not raise_exception))
        return webhook

    async def list(self) -> list[WebhookSchema]:
        return await self.crud.list()

    async def update(self, webhook_id: str, webhook: WebhookUpdate) -> WebhookSchema:
        return await self.crud.update(webhook_id, webhook)

    async def delete(self, webhook_id: str) -> None:
        return await self.crud.delete(webhook_id)

    def create_auth_key(self, auth_token: str, payload: Mapping[str, Any]) -> str:
        payload_json = json.dumps(payload)
        key = cast(str, hmac.new(auth_token.encode(), payload_json.encode(), hashlib.sha256).hexdigest())  # type: ignore
        return key

    async def call(
        self,
        webhook_id: str,
        event: EventType,
        payload: Mapping[str, Any],
        web_push_subscription: dict[str, Any] | None = None,
    ) -> WebhookCallResult:
        webhook = await self.read(webhook_id, raise_exception=True)

        webhook_usage = await self.webhook_usage_ctrl.create(
            WebhookUsageCreate(
                webhook_id=webhook_id,
                webpush_subscription_data=web_push_subscription,
            )
        )

        webhook_usage_callback_url = self.webhook_usage_ctrl.get_callback_url(
            webhook_usage.id
        )

        body = {
            "event": event,
            "payload": payload,
            "callback_url": webhook_usage_callback_url,
        }

        async with httpx.AsyncClient() as client:
            auth_key = self.create_auth_key(webhook.auth_token, body)

            headers = {
                "X-Hercule-Auth-Key": auth_key,
                "X-Hercule-Timestamp": str(datetime.datetime.now().timestamp()),
            }

            timeout = httpx.Timeout(10.0, connect=5.0)

            response = await client.post(
                webhook.url, json=body, headers=headers, timeout=timeout
            )

            if response.status_code >= 400:
                await self.webhook_usage_ctrl.update_status(webhook_usage.id, 'error')
                raise HTTPException(
                    status_code=response.status_code, detail=response.text
                )
            
            await self.webhook_usage_ctrl.update_status(webhook_usage.id, 'success')

            return response.json()
