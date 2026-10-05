"""Estructura de los módulos base (ARQ-008) y registro de sus routers (ARQ-006, API-001).

Las comprobaciones por AST se prueban con un caso válido y varios inválidos sintéticos, y cuentan
lo que evaluaron: así no pasan en vacío (B.1). El registro de routers se comprueba sobre el texto
de `main.py` y no sobre `app.routes` ni `openapi()`, que con routers vacíos no dirían nada.
"""

import ast
import importlib
import pathlib
import re

import pytest
from fastapi import APIRouter

APP_DIR = pathlib.Path(__file__).resolve().parents[1] / "app"
MODULES_DIR = APP_DIR / "modules"
MODULES = ("auth", "users", "settings", "admin", "logs")
BASE_MODULES = frozenset(MODULES)
LAYERS = (
    "__init__",
    "router",
    "schemas",
    "service",
    "repository",
    "models",
    "dependencies",
)
FORBIDDEN_SERVICE_IMPORTS = ("sqlalchemy", "asyncpg", "app.core.database")
PREFIX_CONSTANT = "API_V1_PREFIX"
APP_VARIABLE = "app"
EXPECTED_PREFIX = "/api/v1"
_ROUTER_IMPORT = re.compile(r"app\.modules\.([a-z_]+)\.router")


def _forbidden(name: str) -> bool:
    return any(name == root or name.startswith(root + ".") for root in FORBIDDEN_SERVICE_IMPORTS)


def database_imports(source: str) -> list[str]:
    """Imports de un `service.py` que acceden a la sesión de base de datos (ARQ-008)."""
    found: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            found += [alias.name for alias in node.names if _forbidden(alias.name)]
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if _forbidden(module):
                found.append(module)
            elif module == "app.core":
                found += [f"app.core.{a.name}" for a in node.names if a.name == "database"]
    return found


def _router_aliases(tree: ast.Module) -> dict[str, str]:
    """alias local -> módulo, para `from app.modules.<m>.router import router as <alias>`."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        match = (
            _ROUTER_IMPORT.fullmatch(node.module or "")
            if isinstance(node, ast.ImportFrom)
            else None
        )
        if isinstance(node, ast.ImportFrom) and match:
            for imported in node.names:
                if imported.name == "router":
                    aliases[imported.asname or imported.name] = match.group(1)
    return aliases


def _prefix_value(tree: ast.Module) -> str | None:
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == PREFIX_CONSTANT for t in node.targets)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            return node.value.value
    return None


def _uses_prefix_constant(call: ast.Call) -> bool:
    return any(
        keyword.arg == "prefix"
        and isinstance(keyword.value, ast.Name)
        and keyword.value.id == PREFIX_CONSTANT
        for keyword in call.keywords
    )


def _registered_modules(tree: ast.Module, aliases: dict[str, str]) -> set[str]:
    registered: set[str] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "include_router"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == APP_VARIABLE
            and node.args
            and isinstance(node.args[0], ast.Name)
            and node.args[0].id in aliases
            and _uses_prefix_constant(node)
        ):
            registered.add(aliases[node.args[0].id])
    return registered


def _existing_modules() -> frozenset[str]:
    """Módulos presentes en `app/modules` (directorios que son paquetes)."""
    return frozenset(path.parent.name for path in MODULES_DIR.glob("*/__init__.py"))


def registration_problems(
    source: str, existing_modules: frozenset[str]
) -> tuple[int, set[str], list[str]]:
    """(routers evaluados, módulos registrados, problemas): cada router de módulo importado debe
    incluirse en la aplicación (`app.include_router`, no en otro objeto) con
    `prefix=API_V1_PREFIX`; todo módulo de `existing_modules` debe tener su router importado, y
    esa constante debe valer `/api/v1`."""
    tree = ast.parse(source)
    aliases = _router_aliases(tree)
    registered = _registered_modules(tree, aliases)
    imported = set(aliases.values())
    problems = [
        f"{module}: router sin registrar con prefix={PREFIX_CONSTANT}"
        for module in sorted(imported - registered)
    ]
    problems += [
        f"{module}: módulo en app/modules sin su router importado en main.py"
        for module in sorted(existing_modules - imported)
    ]
    if _prefix_value(tree) != EXPECTED_PREFIX:
        problems.append(f"{PREFIX_CONSTANT} debe valer {EXPECTED_PREFIX!r}")
    return len(aliases), registered, problems


def _main_source(
    *,
    skip: str | None = None,
    other: str | None = None,
    prefix: str | None = PREFIX_CONSTANT,
    constant: str = '"/api/v1"',
) -> str:
    """`main.py` sintético. `skip`: módulo sin `include_router`; `other`: módulo incluido en un
    objeto distinto de `app`; `prefix=None` omite el argumento."""
    lines = [f"from app.modules.{m}.router import router as {m}_router" for m in MODULES]
    lines += [f"{PREFIX_CONSTANT} = {constant}", "def create_app(app, otro):"]
    argument = "" if prefix is None else f", prefix={prefix}"
    for module in MODULES:
        receiver = "otro" if module == other else APP_VARIABLE
        if module != skip:
            lines.append(f"    {receiver}.include_router({module}_router{argument})")
    return "\n".join(lines)


@pytest.mark.parametrize("module", MODULES)
def test_module_has_all_its_layers(module: str) -> None:
    missing = [layer for layer in LAYERS if not (MODULES_DIR / module / f"{layer}.py").is_file()]

    assert missing == []


@pytest.mark.parametrize("module", MODULES)
def test_module_exposes_an_api_router(module: str) -> None:
    router = importlib.import_module(f"app.modules.{module}.router").router

    assert isinstance(router, APIRouter)


def test_main_registers_every_module_router_under_the_api_prefix() -> None:
    """Cota mínima: los módulos de dominio que se agreguen no rompen la prueba, pero tienen que
    estar registrados."""
    existing = _existing_modules()

    evaluated, registered, problems = registration_problems(
        (APP_DIR / "main.py").read_text(), existing
    )

    assert set(MODULES) <= registered
    assert existing <= registered
    assert evaluated >= len(MODULES)
    assert problems == []


def test_valid_synthetic_main_has_no_problems() -> None:
    evaluated, registered, problems = registration_problems(_main_source(), BASE_MODULES)

    assert (evaluated, registered, problems) == (len(MODULES), set(MODULES), [])


def test_module_present_but_not_imported_in_main_is_detected() -> None:
    evaluated, registered, problems = registration_problems(
        _main_source(), BASE_MODULES | {"facturas"}
    )

    assert evaluated == len(MODULES)
    assert registered == set(MODULES)
    assert problems == ["facturas: módulo en app/modules sin su router importado en main.py"]


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        (_main_source(skip="logs"), ["logs: router sin registrar con prefix=API_V1_PREFIX"]),
        (
            _main_source(prefix='"/api/v1"'),
            [f"{m}: router sin registrar con prefix=API_V1_PREFIX" for m in sorted(MODULES)],
        ),
        (
            _main_source(prefix=None),
            [f"{m}: router sin registrar con prefix=API_V1_PREFIX" for m in sorted(MODULES)],
        ),
        (_main_source(constant='"/api/v2"'), ["API_V1_PREFIX debe valer '/api/v1'"]),
        (_main_source(other="auth"), ["auth: router sin registrar con prefix=API_V1_PREFIX"]),
    ],
    ids=[
        "router_sin_registrar",
        "prefijo_literal",
        "sin_prefijo",
        "constante_con_otro_valor",
        "registrado_en_otro_objeto",
    ],
)
def test_invalid_synthetic_main_is_detected(source: str, expected: list[str]) -> None:
    evaluated, _, problems = registration_problems(source, BASE_MODULES)

    assert evaluated == len(MODULES)
    assert problems == expected


@pytest.mark.parametrize("module", MODULES)
def test_service_does_not_import_the_database_session(module: str) -> None:
    source = (MODULES_DIR / module / "service.py").read_text()

    assert database_imports(source) == []


def test_all_base_services_were_evaluated() -> None:
    """Los 5 `service.py` base existen, así que la comprobación de arriba evaluó los 5."""
    services = [MODULES_DIR / module / "service.py" for module in MODULES]

    assert len(services) == len(MODULES) == 5
    assert all(path.is_file() for path in services)


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("import sqlalchemy", ["sqlalchemy"]),
        ("from sqlalchemy.ext.asyncio import AsyncSession", ["sqlalchemy.ext.asyncio"]),
        ("import asyncpg", ["asyncpg"]),
        ("import app.core.database", ["app.core.database"]),
        ("from app.core.database import Database", ["app.core.database"]),
        ("from app.core import database", ["app.core.database"]),
        ("from app.core import database as db", ["app.core.database"]),
    ],
)
def test_database_import_is_detected(source: str, expected: list[str]) -> None:
    assert database_imports(source) == expected


def test_clean_service_source_has_no_database_imports() -> None:
    source = "import json\nfrom app.core.errors import AppError\nfrom app.core import config\n"

    assert database_imports(source) == []
