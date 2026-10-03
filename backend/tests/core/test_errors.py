import httpx
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

from app.core.errors import (
    AppError,
    ErrorBody,
    ErrorEnvelope,
    ServiceUnavailableError,
    UnauthorizedError,
    register_error_handlers,
)
from app.core.tracing import TraceIdMiddleware
from tests.conftest import build_client

LEAK_PROBE = "detalle-interno-que-no-debe-salir"


class _Entrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nombre: str = Field(max_length=10)


class _SampleBusinessError(AppError):
    status_code = 400
    code = "PROYECTO_YA_ARCHIVADO"
    message = "El proyecto ya está archivado."


def _app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(TraceIdMiddleware)
    register_error_handlers(app)

    @app.post("/crear")
    async def crear(entrada: _Entrada) -> dict[str, str]:
        return {"nombre": entrada.nombre}

    @app.get("/negocio")
    async def negocio() -> None:
        raise _SampleBusinessError

    @app.get("/sin-sesion")
    async def sin_sesion() -> None:
        raise UnauthorizedError

    @app.get("/caida")
    async def caida() -> None:
        raise ServiceUnavailableError

    @app.get("/boom")
    async def boom() -> None:
        raise RuntimeError(LEAK_PROBE)

    return app


async def _request(method: str, path: str, json: dict[str, str] | None = None) -> httpx.Response:
    async with build_client(_app()) as client:
        return await client.request(method, path, json=json)


def _assert_envelope(response: httpx.Response, status: int, code: str) -> ErrorBody:
    """Valida la respuesta contra el modelo del envelope (API-005) y devuelve el error tipado."""
    assert response.status_code == status
    assert set(response.json()) == {"error"}
    error = ErrorEnvelope.model_validate(response.json()).error
    assert error.code == code
    assert error.message
    assert error.trace_id == response.headers["X-Trace-Id"]
    assert "Traceback" not in response.text
    assert LEAK_PROBE not in response.text
    return error


async def test_validation_error_lists_fields_without_input_values() -> None:
    response = await _request("POST", "/crear", json={"nombre": "x" * 50, "extra": "valor-secreto"})

    error = _assert_envelope(response, 422, "VALIDATION_ERROR")
    assert error.details is not None
    assert {detail.field for detail in error.details} == {"body.nombre", "body.extra"}
    assert "valor-secreto" not in response.text


async def test_not_found_uses_envelope() -> None:
    response = await _request("GET", "/no-existe")

    error = _assert_envelope(response, 404, "NOT_FOUND")
    assert error.details is None
    assert "details" not in response.json()["error"]


async def test_method_not_allowed_is_reported_with_an_allowed_code() -> None:
    _assert_envelope(await _request("DELETE", "/negocio"), 404, "NOT_FOUND")


async def test_unhandled_error_is_generic() -> None:
    _assert_envelope(await _request("GET", "/boom"), 500, "INTERNAL_ERROR")


async def test_app_errors_keep_their_status_and_code() -> None:
    _assert_envelope(await _request("GET", "/negocio"), 400, "PROYECTO_YA_ARCHIVADO")
    _assert_envelope(await _request("GET", "/sin-sesion"), 401, "UNAUTHORIZED")
    _assert_envelope(await _request("GET", "/caida"), 503, "SERVICE_UNAVAILABLE")
