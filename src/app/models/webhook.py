import uuid as uuid_pkg
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base
from ..core.db.models import UUIDMixin, TimestampMixin

class Webhook(Base, UUIDMixin, TimestampMixin, kw_only=True):
    __tablename__ = "webhooks"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    auth_token: Mapped[str] = mapped_column(String(255), nullable=False, default=lambda: str(uuid_pkg.uuid4()))
