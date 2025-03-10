import os
from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from typing import Any, AsyncContextManager, Sequence

from fastapi import Depends, FastAPI, Request
from fastapi.params import Depends as DependsT

from src.app.api import router
from src.app.core.config import EnvironmentOption, settings

from .db.database import session_manager
from .logger import logging

logger = logging.getLogger(__name__)

# -------------- application --------------


async def log_request_info(request: Request):
    try:
        request_body = await request.json()
    except Exception:
        request_body = await request.body()

    logger.info(
        f"{request.method} request to {request.url} metadata\n"
        f"\tHeaders: {request.headers}\n"
        f"\tBody: {request_body}\n"
        f"\tPath Params: {request.path_params}\n"
        f"\tQuery Params: {request.query_params}\n"
    )

def init_config_dir():
    config_dir = settings.CONFIG_DIR
    os.makedirs(config_dir, exist_ok=True)
    return config_dir


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

    init_config_dir()

    router_dependencies: Sequence[DependsT] = []

    if settings.ENVIRONMENT == EnvironmentOption.LOCAL:
        router_dependencies = [Depends(log_request_info)]

    app.include_router(router, dependencies=router_dependencies)
    
    return app