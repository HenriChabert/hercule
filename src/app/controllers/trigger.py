import logging
import re
from typing import Any, List, Literal, Mapping, TypedDict, cast, overload

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.controllers.base import BaseController
from src.app.controllers.webhook import WebhookCallResult, WebhookController
from src.app.crud.trigger import TriggerCRUD
from src.app.models.trigger import Trigger as TriggerModel
from src.app.schemas.trigger import Trigger as TriggerSchema
from src.app.schemas.trigger import TriggerCreate, TriggerCreateClient, TriggerUpdate
from src.app.schemas.webhook import WebhookCreate
from src.app.types.events import EventContext, EventType

logger = logging.getLogger(__name__)


class TriggerController(BaseController[TriggerSchema, TriggerModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.crud = TriggerCRUD(db)

    async def create(self, trigger: TriggerCreateClient) -> TriggerSchema:
        webhook_ctrl = WebhookController(self.db)

        if trigger.webhook_url is not None:
            webhook = await webhook_ctrl.create(WebhookCreate(url=trigger.webhook_url))
            trigger.webhook_id = webhook.id

        if trigger.webhook_id is None:
            raise HTTPException(status_code=422, detail="Webhook should exist")

        try:
            _ = await webhook_ctrl.read(trigger.webhook_id, allow_none=False)
        except HTTPException as e:
            raise HTTPException(status_code=422, detail="Webhook should exist") from e

        trigger_dto = TriggerCreate(**trigger.model_dump(exclude={"webhook_url"}))

        return await self.crud.create(trigger_dto)

    async def read(
        self, trigger_id: str, allow_none: bool = False
    ) -> TriggerSchema | None:
        return await self.crud.read(trigger_id, allow_none)

    async def read_safe(self, trigger_id: str) -> TriggerSchema:
        return await self.crud.read_safe(trigger_id)

    async def list(
        self, event: EventType | None = None, url: str | None = None
    ) -> list[TriggerSchema]:
        triggers_matching: list[TriggerSchema] = []
        event_triggers = await self.crud.list(event=event)
        for trigger in event_triggers:
            if self.should_trigger(trigger, cast(EventContext, {"url": url})):
                triggers_matching.append(trigger)
        return triggers_matching

    async def update(self, trigger_id: str, trigger: TriggerUpdate) -> TriggerSchema:
        return await self.crud.update(trigger_id, trigger)

    async def delete(self, trigger_id: str) -> None:
        return await self.crud.delete(trigger_id)

    def should_trigger(self, trigger: TriggerSchema, context: EventContext) -> bool:
        if trigger.url_regex is not None:
            url = context.get("url")
            if url is not None and not re.match(trigger.url_regex, url):
                return False

        return True

    async def trigger(
        self,
        trigger_id: str,
        event: EventType,
        context: EventContext,
        web_push_subscription: dict[str, Any] | None = None,
    ) -> WebhookCallResult:
        trigger = await self.read_safe(trigger_id)
        webhook_ctrl = WebhookController(self.db)

        if trigger.webhook_id is None:
            raise HTTPException(status_code=422, detail="Trigger should have a webhook")

        if not self.should_trigger(trigger, context):
            raise HTTPException(status_code=422, detail="Trigger has been filtered out")

        return await webhook_ctrl.call(
            trigger.webhook_id, event, context, web_push_subscription
        )

    async def trigger_event(
        self,
        event: EventType,
        context: EventContext,
        web_push_subscription: dict[str, Any] | None = None,
    ) -> List[WebhookCallResult]:
        triggers_results: list[WebhookCallResult] = []
        if "trigger_id" in context:
            triggers = [await self.read_safe(context["trigger_id"])]
        else:
            triggers = await self.list(event=event)

        triggers_to_trigger: list[TriggerSchema] = []

        for trigger in triggers:
            if self.should_trigger(trigger, context):
                triggers_to_trigger.append(trigger)

        for trigger in triggers_to_trigger:
            trigger_result = await self.trigger(
                trigger.id, event, context, web_push_subscription
            )
            triggers_results.append(trigger_result)

        return triggers_results
