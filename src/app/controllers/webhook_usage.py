from sqlalchemy.ext.asyncio import AsyncSession

from src.app.controllers.base import BaseController
from src.app.crud.webhook_usage import WebhookUsageCRUD
from src.app.models.webhook_usage import WebhookUsage as WebhookUsageModel
from src.app.schemas.webhook_usage import WebhookUsage as WebhookUsageSchema


class WebhookUsageController(BaseController[WebhookUsageSchema, WebhookUsageModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.crud = WebhookUsageCRUD(db)
