"""Endpoint de salud (OPS-004), fuera de `/api/v1/` y de la lista de recursos (API-002)."""

from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.database import Database, get_database
from app.core.errors import ErrorEnvelope

router = APIRouter()


class HealthStatus(BaseModel):
    status: str


class HealthResponse(BaseModel):
    data: HealthStatus


@router.get(
    "/health",
    summary="Estado del servicio",
    description=(
        "Indica que el proceso está vivo y que la base de datos responde. "
        "Si la base de datos no responde, devuelve 503. No expone versiones ni configuración."
    ),
    response_model=HealthResponse,
    status_code=200,
    responses={503: {"model": ErrorEnvelope, "description": "La base de datos no responde."}},
    # Exención de espejo (ARQ-004): visible en el OpenAPI y verificable en el CI.
    openapi_extra={"x-mirror-exempt": "health"},
)
async def health(database: Annotated[Database, Depends(get_database)]) -> HealthResponse:
    await database.ping()
    return HealthResponse(data=HealthStatus(status="ok"))
