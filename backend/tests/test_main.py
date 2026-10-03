import asyncio
import pathlib
import uuid
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager

import pytest
from fastapi import FastAPI
from starlette.requests import Request
from starlette.types import Message

from app.core.config import Settings, get_settings
from app.core.tracing import get_trace_id
from app.main import create_app
from tests.conftest import HealthyDatabase, build_client

UUID_V4 = 4
LIFESPAN_TIMEOUT_SECONDS = 10
PRODUCTION = {
    "APP_ENV": "production",
    "CORS_ALLOWED_ORIGINS": "https://peervibe.cl",
    "SUPABASE_URL": "https://proyecto.supabase.co",
}


@pytest.mark.parametrize("path", ["/docs", "/redoc", "/openapi.json"])
@pytest.mark.parametrize("environment", [PRODUCTION, {}], ids=["production", "development"])
async def test_interactive_docs_and_public_openapi_are_off(
    make_settings: Callable[..., Settings], environment: dict[str, str], path: str
) -> None:
    """SEC-019: documentación interactiva y OpenAPI público desactivados, sin depender del
    entorno (OPS-002)."""
    app = create_app(settings=make_settings(**environment), database=HealthyDatabase())

    async with build_client(app) as client:
        response = await client.get(path)

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"


def test_debug_mode_is_never_enabled(make_settings: Callable[..., Settings]) -> None:
    app = create_app(settings=make_settings(**PRODUCTION), database=HealthyDatabase())

    assert app.debug is False
    assert app.docs_url is None
    assert app.redoc_url is None
    assert app.openapi_url is None


def test_openapi_schema_is_still_available_for_client_generation() -> None:
    """ARQ-010: el cliente se genera desde `app.openapi()`, no desde una URL pública."""
    paths = create_app(database=HealthyDatabase()).openapi()["paths"]

    assert "/health" in paths


@asynccontextmanager
async def _running_lifespan(app: FastAPI) -> AsyncIterator[list[str]]:
    """Ejecuta el lifespan por el stack ASGI completo (middleware incluido), como un servidor."""
    inbox: asyncio.Queue[Message] = asyncio.Queue()
    events: list[str] = []
    startup_finished = asyncio.Event()

    async def receive() -> Message:
        return await inbox.get()

    async def send(message: Message) -> None:
        events.append(message["type"])
        if message["type"].startswith("lifespan.startup"):
            startup_finished.set()

    task = asyncio.create_task(app({"type": "lifespan"}, receive, send))
    await inbox.put({"type": "lifespan.startup"})
    async with asyncio.timeout(LIFESPAN_TIMEOUT_SECONDS):
        await startup_finished.wait()
    try:
        yield events
    finally:
        await inbox.put({"type": "lifespan.shutdown"})
        async with asyncio.timeout(LIFESPAN_TIMEOUT_SECONDS):
            await task


@pytest.mark.integration
async def test_app_creates_and_closes_its_own_database_through_the_lifespan() -> None:
    """Sin base de datos inyectada: el lifespan crea el motor desde la configuración (`.env`
    local) y `/health` responde contra el Supabase local."""
    app = create_app()

    async with _running_lifespan(app) as events, build_client(app) as client:
        response = await client.get("/health")

    assert events == ["lifespan.startup.complete", "lifespan.shutdown.complete"]
    assert response.status_code == 200
    assert response.json() == {"data": {"status": "ok"}}
    assert response.headers["X-Trace-Id"]


async def test_health_is_503_when_the_database_dependency_is_missing() -> None:
    app = create_app(database=HealthyDatabase())
    app.state.database = object()

    async with build_client(app) as client:
        response = await client.get("/health")

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "SERVICE_UNAVAILABLE"


def test_get_trace_id_falls_back_to_a_new_uuid_without_the_middleware() -> None:
    request = Request({"type": "http", "headers": []})

    assert uuid.UUID(get_trace_id(request)).version == UUID_V4


def test_get_settings_is_cached_until_cleared(
    clean_env: pytest.MonkeyPatch, tmp_path: pathlib.Path
) -> None:
    # Sin `.env` en el directorio de trabajo: solo cuentan las variables del proceso.
    clean_env.chdir(tmp_path)

    first = get_settings()
    clean_env.setenv("RATE_LIMIT_READ", "1/second")
    assert get_settings() is first
    assert first.rate_limit_read == "300/minute"

    get_settings.cache_clear()
    assert get_settings().rate_limit_read == "1/second"
