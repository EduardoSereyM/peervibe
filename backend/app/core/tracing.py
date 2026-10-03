"""Trazabilidad por request (API-013): un `trace_id` por request, en header y en errores."""

import re
import uuid

from starlette.datastructures import Headers, MutableHeaders
from starlette.requests import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send

TRACE_ID_HEADER = "X-Trace-Id"

# Solo se acepta del cliente un UUID canónico: largo fijo y sin caracteres de control, para que
# el valor sea seguro en headers y en logs.
_TRACE_ID_PATTERN = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)


def resolve_trace_id(received: list[str]) -> str:
    """Conserva el trace_id del cliente si es un único UUID canónico; si no, genera uno."""
    if len(received) == 1 and _TRACE_ID_PATTERN.fullmatch(received[0]):
        return received[0].lower()
    return str(uuid.uuid4())


def get_trace_id(request: Request) -> str:
    trace_id = request.scope.get("state", {}).get("trace_id")
    if isinstance(trace_id, str):
        return trace_id
    return str(uuid.uuid4())


class TraceIdMiddleware:
    """Middleware ASGI puro: asigna el trace_id al scope y lo agrega a toda respuesta."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        trace_id = resolve_trace_id(Headers(scope=scope).getlist(TRACE_ID_HEADER))
        scope.setdefault("state", {})["trace_id"] = trace_id

        async def send_with_trace_id(message: Message) -> None:
            if message["type"] == "http.response.start":
                MutableHeaders(scope=message)[TRACE_ID_HEADER] = trace_id
            await send(message)

        await self.app(scope, receive, send_with_trace_id)
