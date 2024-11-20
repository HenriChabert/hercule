from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, TypeVar, Generic
from abc import ABC, abstractmethod
from pydantic import BaseModel
from src.app.core.db.database import Base
from src.app.core.sentinel import NOT_PROVIDED

SchemaType = TypeVar("SchemaType", bound=BaseModel)
ModelType = TypeVar("ModelType", bound=Base)

class BaseCRUD(ABC, Generic[SchemaType, ModelType]):
    def __init__(self, db: AsyncSession):
        self.db = db

    @abstractmethod
    def model_to_schema(self, model: ModelType) -> SchemaType:
        pass

    @abstractmethod
    async def list(self, **kwargs: Any) -> list[SchemaType]:
        pass

    @abstractmethod
    async def create(self, data: Any) -> SchemaType:
        pass

    @abstractmethod
    async def read(self, id: str, raise_exception: bool = False) -> SchemaType | None: ...

    @abstractmethod
    async def update(self, id: str, data: Any) -> SchemaType:
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        pass

    def is_param_provided(self, param: Any) -> bool:
        return param is not NOT_PROVIDED

    def only_provided_params(self, params: BaseModel) -> dict[str, Any]:
        return {k: v for k, v in params.model_dump().items() if self.is_param_provided(v)}
