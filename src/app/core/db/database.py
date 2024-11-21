import os
from typing import Any, AsyncGenerator, Type, TypeVar
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, sessionmaker, Session
from src.app.core.logger import logging

logger = logging.getLogger(__name__)

from ..config import settings

T = TypeVar('T', bound=DeclarativeBase)

class Base(DeclarativeBase, MappedAsDataclass):
    pass

class ModelMixin(DeclarativeBase):
  # we build a mixin with a common method we would like to impl
  @classmethod
  def get_or_create(cls: Type[T], *_, **kwargs: Any) -> T:
    context_id = kwargs.get("id")
    _session = Session.object_session(cls)
    if not _session:
        raise ValueError("Session not found")
    _object = _session.query(cls).filter_by(id=context_id).first()
    if not _object:
      _object = cls(**kwargs)
      _session.add(_object)
      _session.commit()
    return _object

DATABASE_URI = settings.SQLITE_URI

async_engine = create_async_engine(
    f"{settings.SQLITE_ASYNC_PREFIX}{DATABASE_URI}", echo=False, future=True
)
sync_engine = create_engine(
    f"{settings.SQLITE_SYNC_PREFIX}{DATABASE_URI}", echo=False, future=True
)


def create_config_dir_if_not_exists() -> None:
    if not os.path.exists(settings.ABSOLUTE_CONFIG_DIR):
        print(f"Creating config directory: {settings.ABSOLUTE_CONFIG_DIR}")
        logger.info(f"Creating config directory: {settings.ABSOLUTE_CONFIG_DIR}")
        os.makedirs(settings.ABSOLUTE_CONFIG_DIR, exist_ok=True)


def clean_db() -> None:
    if os.path.exists(settings.SQLITE_URI):
        print(f"Removing database: {settings.SQLITE_URI}")
        os.remove(settings.SQLITE_URI)
    sync_engine.dispose()


def reinit_db() -> None:
    clean_db()
    create_config_dir_if_not_exists()
    Base.metadata.create_all(sync_engine)


def sync_get_db() -> Session:
    sync_session = sessionmaker(
        bind=sync_engine, class_=Session, expire_on_commit=False
    )
    session = sync_session()
    return session


async def async_get_db() -> AsyncGenerator[AsyncSession]:
    local_session = async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async_session = local_session

    async with async_session() as db:
        yield db


async def init_db() -> None:
    create_config_dir_if_not_exists()

    logger.info(f"Creating database: {settings.SQLITE_URI}")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
