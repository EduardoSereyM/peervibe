"""Convención de `operationId` del OpenAPI (ARQ-010, NOM-001, NOM-002).

La revisión se prueba con un caso válido y un caso inválido por cada motivo, y cuenta las
operaciones que evaluó: así no pasa en vacío (B.1). En el spec real solo se exige una cota mínima,
porque los routers de los módulos todavía no tienen endpoints.
"""

import re
from collections import Counter
from collections.abc import Callable
from enum import Enum
from typing import Any

import pytest
from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute

from app.core.openapi import operation_id
from app.main import API_V1_PREFIX, create_app

HTTP_METHODS = ("get", "put", "post", "delete", "options", "head", "patch", "trace")
SNAKE_CASE = re.compile(r"[a-z][a-z0-9_]*")
DUPLICATE_WARNING = r"Duplicate Operation ID users_listar for function listar"


def _single_operation_problems(
    where: str, operation: dict[str, Any], path: str, counts: Counter[str | None]
) -> list[str]:
    found: list[str] = []
    current = operation.get("operationId")
    if not current:
        return [f"{where}: sin operationId"]
    if counts[current] > 1:
        found.append(f"{where}: operationId duplicado ({current})")
    if not SNAKE_CASE.fullmatch(current):
        found.append(f"{where}: operationId fuera de snake_case ({current})")
    if path.startswith(f"{API_V1_PREFIX}/"):
        tags = operation.get("tags", [])
        if len(tags) != 1:
            found.append(f"{where}: se esperaba exactamente un tag y hay {len(tags)}")
        elif not current.startswith(f"{tags[0]}_"):
            found.append(f"{where}: operationId sin el prefijo del tag ({current})")
    return found


def operation_problems(spec: dict[str, Any]) -> tuple[int, list[str]]:
    """(operaciones evaluadas, problemas) de un OpenAPI, por cada operación HTTP."""
    operations = [
        (path, method, operation)
        for path, item in spec["paths"].items()
        for method, operation in item.items()
        if method in HTTP_METHODS
    ]
    counts = Counter(operation.get("operationId") for _, _, operation in operations)
    problems: list[str] = []
    for path, method, operation in operations:
        problems += _single_operation_problems(f"{method.upper()} {path}", operation, path, counts)
    return len(operations), problems


async def listar() -> dict[str, str]:
    return {}


async def export_data() -> dict[str, str]:
    return {}


def _router(tags: list[str | Enum] | None, *paths_and_endpoints: tuple[str, Any]) -> APIRouter:
    router = APIRouter(tags=tags)
    for path, endpoint in paths_and_endpoints:
        router.add_api_route(path, endpoint, methods=["GET"])
    return router


def _spec(
    *routers: APIRouter, id_function: Callable[[APIRoute], str] = operation_id
) -> dict[str, Any]:
    app = FastAPI(generate_unique_id_function=id_function)
    for router in routers:
        app.include_router(router, prefix=API_V1_PREFIX)
    return app.openapi()


def test_same_function_in_two_modules_gives_distinct_valid_ids() -> None:
    spec = _spec(
        _router(["users"], ("/users/export", export_data)),
        _router(["auth"], ("/auth/export", export_data)),
    )

    evaluated, problems = operation_problems(spec)

    ids = {op["operationId"] for item in spec["paths"].values() for op in item.values()}
    assert ids == {"users_export_data", "auth_export_data"}
    assert evaluated == 2
    assert problems == []


def test_duplicate_operation_id_in_one_module_is_a_problem() -> None:
    router = _router(["users"], ("/users", listar), ("/users/todos", listar))

    with pytest.warns(UserWarning, match=DUPLICATE_WARNING):
        spec = _spec(router)

    evaluated, problems = operation_problems(spec)

    assert evaluated == 2
    assert problems == [
        "GET /api/v1/users: operationId duplicado (users_listar)",
        "GET /api/v1/users/todos: operationId duplicado (users_listar)",
    ]


def test_route_under_api_v1_without_tag_is_a_problem() -> None:
    evaluated, problems = operation_problems(_spec(_router(None, ("/users", listar))))

    assert evaluated == 1
    assert problems == ["GET /api/v1/users: se esperaba exactamente un tag y hay 0"]


def test_route_under_api_v1_with_more_than_one_tag_is_a_problem() -> None:
    spec = _spec(_router(["users", "admin"], ("/users", listar)))

    evaluated, problems = operation_problems(spec)

    assert spec["paths"]["/api/v1/users"]["get"]["operationId"] == "users_listar"
    assert evaluated == 1
    assert problems == ["GET /api/v1/users: se esperaba exactamente un tag y hay 2"]


def test_operation_id_without_the_tag_prefix_is_a_problem() -> None:
    spec = _spec(_router(["users"], ("/users", listar)), id_function=lambda route: route.name)

    evaluated, problems = operation_problems(spec)

    assert evaluated == 1
    assert problems == ["GET /api/v1/users: operationId sin el prefijo del tag (listar)"]


def test_operation_id_in_camel_case_is_a_problem() -> None:
    spec = _spec(
        _router(["users"], ("/users", listar)), id_function=lambda route: "users_exportData"
    )

    evaluated, problems = operation_problems(spec)

    assert evaluated == 1
    assert problems == ["GET /api/v1/users: operationId fuera de snake_case (users_exportData)"]


def test_operation_without_operation_id_is_a_problem() -> None:
    evaluated, problems = operation_problems({"paths": {"/health": {"get": {}}}})

    assert evaluated == 1
    assert problems == ["GET /health: sin operationId"]


def test_real_spec_follows_the_convention() -> None:
    spec = create_app().openapi()

    evaluated, problems = operation_problems(spec)

    assert evaluated >= 1
    assert spec["paths"]["/health"]["get"]["operationId"] == "health"
    assert problems == []
