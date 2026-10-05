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
from app.core.openapi import operation_id
from app.core.tracing import TraceIdMiddleware
from app.modules.admin.router import router as admin_router
from app.modules.auth.router import router as auth_router
from app.modules.logs.router import router as logs_router
from app.modules.settings.router import router as settings_router
from app.modules.users.router import router as users_router

API_V1_PREFIX = "/api/v1"


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
        generate_unique_id_function=operation_id,
    )
    if database:
        app.state.database = database
    app.add_middleware(TraceIdMiddleware)
    register_error_handlers(app)
    app.include_router(health_router)
    app.include_router(auth_router, prefix=API_V1_PREFIX)
    app.include_router(users_router, prefix=API_V1_PREFIX)
    app.include_router(settings_router, prefix=API_V1_PREFIX)
    app.include_router(admin_router, prefix=API_V1_PREFIX)
    app.include_router(logs_router, prefix=API_V1_PREFIX)
    return app
