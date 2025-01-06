from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base, ModelMixin
from ..core.db.models import IDMixin, TimestampMixin
from ..types.events import EventType

from typing import Literal, TypeAlias

WebhookUsageStatus: TypeAlias = Literal["success", "error", "pending"]

class WebhookUsage(Base, ModelMixin, IDMixin, TimestampMixin, kw_only=True):
    __tablename__ = "webhook_usage"

    webhook_id: Mapped[str] = mapped_column(ForeignKey("webhooks.id"))
    event: Mapped[EventType] = mapped_column(String(255), nullable=False)
    status: Mapped[WebhookUsageStatus] = mapped_column(String(255), nullable=False)

    webpush_subscription_data: Mapped[str] = mapped_column(String(255), nullable=True, default="{}")

    