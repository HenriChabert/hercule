from abc import ABC
from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.database import Base
from src.app.crud.base import BaseCRUD

SchemaType = TypeVar("SchemaType", bound=BaseModel)
ModelType = TypeVar("ModelType", bound=Base)

class BaseController(ABC, Generic[SchemaType, ModelType]):
    db: AsyncSession
    
    def __init__(self, db: AsyncSession):
        self.db = db