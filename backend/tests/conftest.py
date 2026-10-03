from collections.abc import AsyncIterator, Callable, Iterator

import httpx
import pytest
from fastapi import FastAPI

from app.core.config import Settings, get_settings
from app.core.database import Database, create_user_engine

CLOSED_PORT_URL = "postgresql+asyncpg://sintetico:sintetico@127.0.0.1:1/sintetica"

# Valores sintéticos (DB-018): no corresponden a ningún entorno real.
VALID_ENV: dict[str, str] = {
    "APP_ENV": "development",
    "CORS_ALLOWED_ORIGINS": "http://localhost:5173",
    "RATE_LIMIT_AUTH": "10/minute",
    "RATE_LIMIT_WRITE": "60/minute",
    "RATE_LIMIT_READ": "300/minute",
    "SUPABASE_URL": "http://127.0.0.1:54321",
    "SUPABASE_SECRET_KEY": "sb_secret_sintetica",
    "DATABASE_URL": CLOSED_PORT_URL,
    "DATABASE_URL_PRIVILEGED": CLOSED_PORT_URL,
}


class HealthyDatabase(Database):
    """Base de datos de prueba que siempre responde, sin motor ni conexión."""

    def __init__(self) -> None:
        pass

    async def ping(self) -> None:
        return None


@pytest.fixture(autouse=True)
def _reset_settings_cache() -> Iterator[None]:
    """`get_settings` cachea la configuración: ningún test hereda la de otro."""
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def clean_env(monkeypatch: pytest.MonkeyPatch) -> pytest.MonkeyPatch:
    """Deja solo las variables sintéticas válidas, sin leer el `.env` local."""
    for name in list(VALID_ENV):
        monkeypatch.delenv(name, raising=False)
    for name, value in VALID_ENV.items():
        monkeypatch.setenv(name, value)
    return monkeypatch


@pytest.fixture
def make_settings(clean_env: pytest.MonkeyPatch) -> Callable[..., Settings]:
    def build(**overrides: str) -> Settings:
        for name, value in overrides.items():
            clean_env.setenv(name, value)
        return Settings(_env_file=None)

    return build


@pytest.fixture
async def closed_database(make_settings: Callable[..., Settings]) -> AsyncIterator[Database]:
    """Base de datos inalcanzable (puerto cerrado): simula la caída."""
    database = Database(create_user_engine(make_settings()))
    yield database
    await database.dispose()


def build_client(app: FastAPI) -> httpx.AsyncClient:
    transport = httpx.ASGITransport(app=app, raise_app_exceptions=False)
    return httpx.AsyncClient(transport=transport, base_url="http://prueba")
