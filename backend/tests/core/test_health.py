from collections.abc import AsyncIterator

import pytest

from app.core.config import Settings
from app.core.database import Database, create_user_engine
from app.core.errors import ServiceUnavailableError
from app.main import create_app
from tests.conftest import HealthyDatabase, build_client


class _FailingDatabase(HealthyDatabase):
    async def ping(self) -> None:
        raise ServiceUnavailableError


@pytest.fixture
async def local_database() -> AsyncIterator[Database]:
    database = Database(create_user_engine(Settings()))
    yield database
    await database.dispose()


async def test_health_is_ok_with_envelope() -> None:
    async with build_client(create_app(database=HealthyDatabase())) as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"data": {"status": "ok"}}


async def test_health_returns_503_with_envelope_when_database_fails() -> None:
    async with build_client(create_app(database=_FailingDatabase())) as client:
        response = await client.get("/health")

    assert response.status_code == 503
    error = response.json()["error"]
    assert error["code"] == "SERVICE_UNAVAILABLE"
    assert error["trace_id"] == response.headers["X-Trace-Id"]


async def test_health_returns_503_when_database_is_unreachable(closed_database: Database) -> None:
    async with build_client(create_app(database=closed_database)) as client:
        response = await client.get("/health")

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "SERVICE_UNAVAILABLE"
    assert "127.0.0.1" not in response.text


@pytest.mark.integration
async def test_health_is_ok_against_local_database(local_database: Database) -> None:
    async with build_client(create_app(database=local_database)) as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"data": {"status": "ok"}}


def test_health_is_marked_as_mirror_exempt_and_is_public() -> None:
    operation = create_app(database=HealthyDatabase()).openapi()["paths"]["/health"]["get"]

    assert operation["x-mirror-exempt"] == "health"
    assert operation["summary"]
    assert "503" in operation["responses"]
    assert "security" not in operation
