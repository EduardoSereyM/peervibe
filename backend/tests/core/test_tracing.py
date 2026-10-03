import uuid

import httpx
import pytest
from fastapi import FastAPI

from app.core.errors import register_error_handlers
from app.core.tracing import TRACE_ID_HEADER, TraceIdMiddleware, resolve_trace_id
from tests.conftest import build_client

VALID_TRACE_ID = "3f2b8c1e-5d4a-4e6b-9a7c-1b2d3e4f5a6b"


def _app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(TraceIdMiddleware)
    register_error_handlers(app)

    @app.get("/ok")
    async def ok() -> dict[str, str]:
        return {"estado": "ok"}

    @app.get("/falla")
    async def falla() -> None:
        raise RuntimeError

    return app


async def _get(path: str, headers: dict[str, str] | None = None) -> httpx.Response:
    async with build_client(_app()) as client:
        return await client.get(path, headers=headers)


async def test_absent_trace_id_is_generated() -> None:
    response = await _get("/ok")

    assert str(uuid.UUID(response.headers[TRACE_ID_HEADER])) == response.headers[TRACE_ID_HEADER]


async def test_valid_trace_id_is_kept() -> None:
    response = await _get("/ok", {TRACE_ID_HEADER: VALID_TRACE_ID})

    assert response.headers[TRACE_ID_HEADER] == VALID_TRACE_ID


async def test_valid_trace_id_is_normalized_to_lowercase() -> None:
    response = await _get("/ok", {TRACE_ID_HEADER: VALID_TRACE_ID.upper()})

    assert response.headers[TRACE_ID_HEADER] == VALID_TRACE_ID


@pytest.mark.parametrize(
    "invalid",
    [
        "no-es-un-uuid",
        VALID_TRACE_ID + "0",
        VALID_TRACE_ID.replace("-", ""),
        "{" + VALID_TRACE_ID + "}",
        "urn:uuid:" + VALID_TRACE_ID,
        "x" * 500,
        " " + VALID_TRACE_ID,
    ],
)
async def test_invalid_trace_id_is_replaced(invalid: str) -> None:
    response = await _get("/ok", {TRACE_ID_HEADER: invalid})

    assert response.headers[TRACE_ID_HEADER] != invalid
    assert uuid.UUID(response.headers[TRACE_ID_HEADER])


def test_repeated_or_control_character_values_are_replaced() -> None:
    assert resolve_trace_id([VALID_TRACE_ID, VALID_TRACE_ID]) != VALID_TRACE_ID
    assert resolve_trace_id([VALID_TRACE_ID + "\n"]) != VALID_TRACE_ID
    assert resolve_trace_id([]) != resolve_trace_id([])


async def test_trace_id_is_in_header_and_error_envelope() -> None:
    response = await _get("/no-existe", {TRACE_ID_HEADER: VALID_TRACE_ID})

    assert response.status_code == 404
    assert response.headers[TRACE_ID_HEADER] == VALID_TRACE_ID
    assert response.json()["error"]["trace_id"] == VALID_TRACE_ID


async def test_trace_id_is_in_header_and_envelope_of_unhandled_error() -> None:
    response = await _get("/falla", {TRACE_ID_HEADER: VALID_TRACE_ID})

    assert response.status_code == 500
    assert response.headers[TRACE_ID_HEADER] == VALID_TRACE_ID
    assert response.json()["error"]["trace_id"] == VALID_TRACE_ID


async def test_generated_trace_id_matches_between_header_and_envelope() -> None:
    response = await _get("/no-existe")

    assert response.json()["error"]["trace_id"] == response.headers[TRACE_ID_HEADER]
