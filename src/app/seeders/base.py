from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
from typing import Any, Mapping

class BaseSeeder(ABC):
    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def seed(self, n: int = 1, fields: Any | None = None) -> list[Any]:
        pass
