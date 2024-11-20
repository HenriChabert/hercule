import uuid as uuid_pkg

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base
from ..core.db.models import IDMixin, TimestampMixin

class Trigger(Base, IDMixin, TimestampMixin, kw_only=True):
    __tablename__ = "triggers"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    webhook_id: Mapped[str] = mapped_column(ForeignKey("webhooks.id"))
    url_regex: Mapped[str] = mapped_column(String(255), nullable=True, default=None)

    
