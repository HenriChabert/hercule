from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod
from typing import Any, Mapping

class BaseSeeder(ABC):
    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def seed(self, n: int = 1, fields: Any | None = None) -> list[Any]:
        pass
