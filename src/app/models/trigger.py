import uuid as uuid_pkg
from typing import Literal, TypeAlias

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base, ModelMixin
from ..core.db.models import IDMixin, TimestampMixin
from ..types.events import EventType

TriggerSource: TypeAlias = Literal["n8n", "zapier"]


class Trigger(Base, ModelMixin, IDMixin, TimestampMixin, kw_only=True):
    __tablename__ = "triggers"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    webhook_id: Mapped[str | None] = mapped_column(
        ForeignKey("webhooks.id"), nullable=True
    )
    source: Mapped[TriggerSource] = mapped_column(String(255), nullable=False)
    event: Mapped[EventType] = mapped_column(String(255), nullable=False)
    url_regex: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
    )
