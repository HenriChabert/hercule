from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base, ModelMixin
from ..core.db.models import IDMixin, TimestampMixin

class User(Base, ModelMixin, IDMixin, TimestampMixin, kw_only=True):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)