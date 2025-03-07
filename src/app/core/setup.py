from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from typing import Any, AsyncContextManager

from fastapi import FastAPI

from src.app.api import router
from src.app.core.config import settings

from .config import Settings
from .db.database import session_manager
from .logger import logging

logger = logging.getLogger(__name__)

# -------------- application --------------


def lifespan_factory(
    create_tables_on_start: bool = True,
) -> Callable[[FastAPI], AsyncContextManager[Any]]:
    """Factory to create a lifespan async context manager for a FastAPI app."""
    session_manager.init(settings.SQLITE_URI)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        if create_tables_on_start:
            logger.info("Creating database tables")
            async with session_manager.connect() as connection:
                await session_manager.create_all(connection)
        yield
        if session_manager._engine is not None: # type: ignore
            await session_manager.close()

    return lifespan

def init_app(
    init_db: bool = True,
    create_tables_on_start: bool = True,
    **kwargs: Any,
) -> FastAPI:
    # --- before creating application ---
    to_update = {
        "title": settings.APP_NAME,
        "description": settings.APP_DESCRIPTION,
        "contact": {"name": settings.CONTACT_NAME, "email": settings.CONTACT_EMAIL},
        "license_info": {"name": settings.LICENSE_NAME},
    }
    kwargs.update(to_update)

    kwargs.update({"docs_url": None, "redoc_url": None, "openapi_url": None})
    
    lifespan: Callable[[FastAPI], AsyncContextManager[Any]] | None = None
    if init_db:
        lifespan = lifespan_factory(create_tables_on_start=create_tables_on_start)

    app = FastAPI(
        lifespan=lifespan,
        **kwargs,
    )

    app.include_router(router)
    
    return app