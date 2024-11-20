import os
from typing import AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, sessionmaker, Session
from ...core.logger import logging

logger = logging.getLogger(__name__)

from ..config import settings


class Base(DeclarativeBase, MappedAsDataclass):
    pass


DATABASE_URI = settings.SQLITE_URI

async_engine = create_async_engine(f"{settings.SQLITE_ASYNC_PREFIX}{DATABASE_URI}", echo=False, future=True)
sync_engine = create_engine(f"{settings.SQLITE_SYNC_PREFIX}{DATABASE_URI}", echo=False, future=True)

def create_config_dir_if_not_exists() -> None:
    if not os.path.exists(settings.CONFIG_DIR):
        print(f"Creating config directory: {settings.CONFIG_DIR}")
        logger.info(f"Creating config directory: {settings.CONFIG_DIR}")
        os.makedirs(settings.CONFIG_DIR, exist_ok=True)

def clean_db() -> None:
    if os.path.exists(settings.SQLITE_URI):
        os.remove(settings.SQLITE_URI)
    sync_engine.dispose()

def reinit_db() -> None:
    clean_db()
    create_config_dir_if_not_exists()
    Base.metadata.create_all(sync_engine)

def sync_get_db() -> Session:
    sync_session = sessionmaker(bind=sync_engine, class_=Session, expire_on_commit=False)
    session = sync_session()
    return session


async def async_get_db() -> AsyncGenerator[AsyncSession]:
    local_session = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)
    async_session = local_session

    async with async_session() as db:
        yield db

async def init_db() -> None:
    create_config_dir_if_not_exists()

    logger.info(f"Creating database: {settings.SQLITE_URI}")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
