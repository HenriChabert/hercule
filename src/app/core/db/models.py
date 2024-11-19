import uuid as uuid_pkg
from datetime import UTC, datetime

from sqlalchemy import Boolean, Column, DateTime, text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass

class UUIDMixin(MappedAsDataclass, kw_only=True):
    id: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID, primary_key=True, default_factory=uuid_pkg.uuid4, server_default=text("gen_random_uuid()"), kw_only=True
    )

class TimestampMixin(MappedAsDataclass, kw_only=True):
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=func.now, kw_only=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=func.now, onupdate=func.now(), kw_only=True)
