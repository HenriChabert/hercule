import uuid as uuid_pkg
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base, ModelMixin
from ..core.db.models import IDMixin, TimestampMixin

class Webhook(Base, ModelMixin, IDMixin, TimestampMixin, kw_only=True):
    __tablename__ = "webhooks"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    auth_token: Mapped[str] = mapped_column(String(255), nullable=False, default=lambda: str(uuid_pkg.uuid4()))
