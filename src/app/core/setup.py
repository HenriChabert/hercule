from typing import Any
from fastapi import FastAPI, APIRouter
from collections.abc import AsyncGenerator, Callable
from contextlib import _AsyncGeneratorContextManager, asynccontextmanager
from .config import AppSettings, DatabaseSettings, EnvironmentSettings, Settings
from .db.database import Base, async_engine as engine, init_db
from .logger import logging

logger = logging.getLogger(__name__)

# -------------- database --------------
async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# -------------- application --------------


def lifespan_factory(
    settings: Settings,
    create_tables_on_start: bool = True,
) -> Callable[[FastAPI], _AsyncGeneratorContextManager[Any]]:
    """Factory to create a lifespan async context manager for a FastAPI app."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator:
        if isinstance(settings, DatabaseSettings) and create_tables_on_start:
            logger.info("Creating database tables")
            await init_db()
        yield

    return lifespan

def create_application(
    router: APIRouter,
    settings: Settings,
    create_tables_on_start: bool = True,
    **kwargs: Any,
) -> FastAPI:
    # --- before creating application ---
    if isinstance(settings, AppSettings):
        to_update = {
            "title": settings.APP_NAME,
            "description": settings.APP_DESCRIPTION,
            "contact": {"name": settings.CONTACT_NAME, "email": settings.CONTACT_EMAIL},
            "license_info": {"name": settings.LICENSE_NAME},
        }
        kwargs.update(to_update)

    if isinstance(settings, EnvironmentSettings):
        kwargs.update({"docs_url": None, "redoc_url": None, "openapi_url": None})
        
    lifespan = lifespan_factory(settings, create_tables_on_start=create_tables_on_start)

    app = FastAPI(
        lifespan=lifespan,
        **kwargs,
    )
    app.include_router(router)
    return app