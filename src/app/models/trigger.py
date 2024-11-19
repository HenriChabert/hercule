import uuid as uuid_pkg
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base
from ..core.db.models import UUIDMixin, TimestampMixin
class Trigger(Base, UUIDMixin, TimestampMixin, kw_only=True):
    __tablename__ = "triggers"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    webhook_id: Mapped[uuid_pkg.UUID] = mapped_column(ForeignKey("webhooks.id"))
    url_regex: Mapped[str] = mapped_column(String(255), nullable=True, default=None)

    
