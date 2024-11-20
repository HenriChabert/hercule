from abc import ABC
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession
from src.app.crud.base import BaseCRUD

from typing import TypeVar, Generic
from src.app.core.db.database import Base

SchemaType = TypeVar("SchemaType", bound=BaseModel)
ModelType = TypeVar("ModelType", bound=Base)

class BaseController(ABC, Generic[SchemaType, ModelType]):
    db: AsyncSession
    crud: BaseCRUD[SchemaType, ModelType]
    
    def __init__(self, db: AsyncSession):
        self.db = db