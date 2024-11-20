import uuid as uuid_pkg
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass

class IDMixin(MappedAsDataclass, kw_only=True):
    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default_factory=lambda: str(uuid_pkg.uuid4()), kw_only=True
    )

class TimestampMixin(MappedAsDataclass, kw_only=True):
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=func.now, kw_only=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=func.now, onupdate=func.now(), kw_only=True)
