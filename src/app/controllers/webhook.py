import httpx
import json
import hmac
import hashlib
import datetime

from fastapi import HTTPException

from src.app.controllers.base import BaseController
from src.app.schemas.webhook import WebhookCreate, Webhook as WebhookSchema, WebhookUpdate
from src.app.models.webhook import Webhook as WebhookModel

from sqlalchemy.ext.asyncio import AsyncSession
from src.app.crud.webhook import WebhookCRUD

from typing import Mapping, Any, overload, Literal, cast, TypedDict

from src.app.types.actions import Action

class WebhookCallResult(TypedDict):
    status: int
    actions: list[Action]

class WebhookController(BaseController[WebhookSchema, WebhookModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.crud = WebhookCRUD(db)

    async def create(self, webhook: WebhookCreate) -> WebhookSchema:
        return await self.crud.create(webhook)
    
    @overload
    async def read(self, webhook_id: str, raise_exception: Literal[False] = False) -> WebhookSchema | None: ...

    @overload
    async def read(self, webhook_id: str, raise_exception: Literal[True]) -> WebhookSchema: ...

    async def read(self, webhook_id: str, raise_exception: bool = False) -> WebhookSchema | None:
        webhook = await self.crud.read(webhook_id, raise_exception=raise_exception)
        return webhook
    
    async def list(self) -> list[WebhookSchema]:
        return await self.crud.list()
    
    async def update(self, webhook_id: str, webhook: WebhookUpdate) -> WebhookSchema:
        return await self.crud.update(webhook_id, webhook)
    
    async def delete(self, webhook_id: str) -> None:
        return await self.crud.delete(webhook_id)

    def create_auth_key(self, auth_token: str, payload: Mapping[str, Any]) -> str:
        payload_json = json.dumps(payload)
        key = cast(str, hmac.new(auth_token.encode(), payload_json.encode(), hashlib.sha256).hexdigest()) # type: ignore
        return key
    
    async def call(self, webhook_id: str, payload: Mapping[str, Any]) -> WebhookCallResult:
        webhook = await self.read(webhook_id, raise_exception=True)
        async with httpx.AsyncClient() as client:
            auth_key = self.create_auth_key(webhook.auth_token, payload)

            headers = {
                "X-Hercule-Auth-Key": auth_key,
                "X-Hercule-Timestamp": str(datetime.datetime.now().timestamp()),
            }

            timeout = httpx.Timeout(10.0, connect=5.0)

            response = await client.post(webhook.url, json=payload, headers=headers, timeout=timeout)
            
            if response.status_code >= 400:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            
            return response.json()
            
            
            
