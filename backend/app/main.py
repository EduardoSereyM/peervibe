"""Punto de composición de la aplicación (ARQ-006): registra middleware, errores y routers.

Se ejecuta con `uvicorn app.main:create_app --factory`: no hay efectos al importar el módulo.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import Settings, get_settings
from app.core.database import Database, create_user_engine
from app.core.errors import register_error_handlers
from app.core.health import router as health_router
from app.core.tracing import TraceIdMiddleware


def create_app(settings: Settings | None = None, database: Database | None = None) -> FastAPI:
    """Con `database` el llamador es dueño de la conexión; sin ella, la app crea y cierra
    la suya."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        owned = Database(create_user_engine(settings or get_settings()))
        app.state.database = owned
        yield
        await owned.dispose()

    # Sin documentación interactiva ni OpenAPI público (SEC-019); el cliente se genera con
    # `app.openapi()` (ARQ-010).
    app = FastAPI(
        title="peervibe",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        lifespan=None if database else lifespan,
    )
    if database:
        app.state.database = database
    app.add_middleware(TraceIdMiddleware)
    register_error_handlers(app)
    app.include_router(health_router)
    return app
