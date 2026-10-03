"""Envelope de error y manejadores globales (API-005, NOM-004)."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.tracing import TRACE_ID_HEADER, get_trace_id

# API-006 limita los códigos HTTP del sistema: cualquier otro se informa como 404.
_HTTP_CODES: dict[int, tuple[str, str]] = {
    401: ("UNAUTHORIZED", "Debes iniciar sesión para continuar."),
    403: ("FORBIDDEN", "No tienes permiso para realizar esta acción."),
    404: ("NOT_FOUND", "El recurso solicitado no existe."),
    409: ("CONFLICT", "La operación entra en conflicto con el estado actual."),
    429: ("RATE_LIMITED", "Demasiadas solicitudes. Intenta de nuevo más tarde."),
    503: ("SERVICE_UNAVAILABLE", "El servicio no está disponible en este momento."),
}
_FALLBACK_HTTP_CODE = 404
_VALIDATION_MESSAGE = "Los datos enviados no son válidos."
_INTERNAL_MESSAGE = "Ocurrió un error interno. Intenta de nuevo más tarde."


class FieldError(BaseModel):
    field: str
    message: str


class ErrorBody(BaseModel):
    code: str
    message: str
    details: list[FieldError] | None = None
    trace_id: str


class ErrorEnvelope(BaseModel):
    error: ErrorBody


class AppError(Exception):
    """Error controlado: la capa que lo lanza no conoce el formato HTTP."""

    status_code = 500
    code = "INTERNAL_ERROR"
    message = _INTERNAL_MESSAGE


class UnauthorizedError(AppError):
    status_code = 401
    code = "UNAUTHORIZED"
    message = _HTTP_CODES[401][1]


class ServiceUnavailableError(AppError):
    status_code = 503
    code = "SERVICE_UNAVAILABLE"
    message = _HTTP_CODES[503][1]


def _describe(exc: Exception) -> tuple[int, str, str, list[FieldError] | None]:
    """(status, code, message, details) de una excepción; nunca expone `str(exc)` ni trazas."""
    if isinstance(exc, AppError):
        return exc.status_code, exc.code, exc.message, None
    if isinstance(exc, RequestValidationError):
        details = [
            FieldError(field=".".join(str(part) for part in error["loc"]), message=error["msg"])
            for error in exc.errors()
        ]
        return 422, "VALIDATION_ERROR", _VALIDATION_MESSAGE, details
    if isinstance(exc, StarletteHTTPException):
        status = exc.status_code if exc.status_code in _HTTP_CODES else _FALLBACK_HTTP_CODE
        code, message = _HTTP_CODES[status]
        return status, code, message, None
    return 500, "INTERNAL_ERROR", _INTERNAL_MESSAGE, None


async def _handle(request: Request, exc: Exception) -> JSONResponse:
    status, code, message, details = _describe(exc)
    trace_id = get_trace_id(request)
    body = ErrorEnvelope(
        error=ErrorBody(code=code, message=message, details=details, trace_id=trace_id)
    )
    # El 500 lo emite el middleware más externo, por fuera del de trazado: el header se fija aquí.
    return JSONResponse(
        body.model_dump(mode="json", exclude_none=True),
        status_code=status,
        headers={TRACE_ID_HEADER: trace_id},
    )


def register_error_handlers(app: FastAPI) -> None:
    for exc_class in (AppError, RequestValidationError, StarletteHTTPException, Exception):
        app.add_exception_handler(exc_class, _handle)
