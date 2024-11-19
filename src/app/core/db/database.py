import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from ...core.logger import logging

logger = logging.getLogger(__name__)

from ..config import settings


class Base(DeclarativeBase, MappedAsDataclass):
    pass


DATABASE_URI = settings.SQLITE_URI
DATABASE_PREFIX = settings.SQLITE_ASYNC_PREFIX
DATABASE_URL = f"{DATABASE_PREFIX}{DATABASE_URI}"

async_engine = create_async_engine(DATABASE_URL, echo=False, future=True)

local_session = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

async def async_get_db() -> AsyncGenerator[AsyncSession]:
    async_session = local_session
    async with async_session() as db:
        yield db

async def init_db() -> None:
    if not os.path.exists(settings.CONFIG_DIR):
        print(f"Creating config directory: {settings.CONFIG_DIR}")
        logger.info(f"Creating config directory: {settings.CONFIG_DIR}")
        os.makedirs(settings.CONFIG_DIR, exist_ok=True)
    
    logger.info(f"Creating database: {settings.SQLITE_URI}")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
