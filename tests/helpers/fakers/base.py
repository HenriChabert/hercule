from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, TypeVar

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.app.core.db.database import Base

T = TypeVar("T", bound=Base)

class BaseFaker(ABC, Generic[T]):
    def __init__(self, fake: Faker | None = None):
        self.fake = fake if fake is not None else Faker()

    @abstractmethod
    def get_fake(self, fields: Any | None = None) -> T:
        pass
    
    @abstractmethod
    async def create_fake(self, db: AsyncSession, fields: Any | None = None) -> T:
        pass

    async def create_fake_object(self, db: AsyncSession, fn: Callable[[Any], T], fields: Any | None = None) -> T:
        obj = fn(fields)
        async with db as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
        return obj
