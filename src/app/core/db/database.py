import os
from typing import Any, Type, TypeVar

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Session

from src.app.core.logger import logging

logger = logging.getLogger(__name__)

import contextlib
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class Base(DeclarativeBase, MappedAsDataclass):
    pass

T = TypeVar('T', bound=DeclarativeBase)

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
  
class SQLiteDatabaseHandler:
    path: str

    def __init__(self, path: str):
        self.path = path

    def _create_db_parent_dir(self):
        os.makedirs(self.path, exist_ok=True)

    @property
    def host(self) -> str:
        return f"{self.path}"
        


class DatabaseSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker[AsyncSession] | None = None

    def init(self, host: str):
        self._engine = create_async_engine(host)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    # Used for testing
    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)

session_manager = DatabaseSessionManager()

async def async_get_db() -> AsyncIterator[AsyncSession]:
    async with session_manager.session() as session:
        yield session