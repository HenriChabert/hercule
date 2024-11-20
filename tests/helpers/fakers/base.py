from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod
from src.app.core.db.database import Base

from typing import Any, Callable, TypeVar, Generic

T = TypeVar("T", bound=Base)

class BaseFaker(ABC, Generic[T]):
    def __init__(self, fake: Faker | None = None):
        self.fake = fake if fake is not None else Faker()

    @abstractmethod
    def get_fake(self, fields: Any | None = None) -> T:
        pass
    
    @abstractmethod
    def create_fake(self, db: Session, fields: Any | None = None) -> T:
        pass

    def create_fake_object(self, db: Session, fn: Callable[[Any], T], fields: Any | None = None) -> T:
        obj = fn(fields)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    async def create_fake_object_async(self, db: AsyncSession, fn: Callable[[Any], T], fields: Any | None = None) -> T:
        obj = fn(fields)
        async with db as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
        return obj
