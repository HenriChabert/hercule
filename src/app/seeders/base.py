from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseSeeder(ABC):
    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def seed(self, n: int = 1, fields: Dict[str, Any] = {}) -> None:
        pass
