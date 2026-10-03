"""Prueba que los contratos de import-linter detectan violaciones (B.1: caso válido e inválido).

Cada caso crea un paquete `app` temporal con la misma configuración de contratos del proyecto y
un único import prohibido; import-linter debe fallar. El caso válido debe pasar.
"""

import pathlib
import subprocess
import sys
import tomllib

import pytest

BACKEND_DIR = pathlib.Path(__file__).resolve().parents[2]
MODULES = ("auth", "users", "settings", "admin", "logs")
_LAYER_PACKAGES = ("core", "shared", "modules")


def _project_contracts() -> str:
    """Copia la sección [tool.importlinter] real, para probar los contratos reales."""
    config = tomllib.loads((BACKEND_DIR / "pyproject.toml").read_text())["tool"]["importlinter"]
    lines = ["[tool.importlinter]"]
    lines.append(f'root_package = "{config["root_package"]}"')
    lines.append(f"include_external_packages = {str(config['include_external_packages']).lower()}")
    for contract in config["contracts"]:
        lines.append("\n[[tool.importlinter.contracts]]")
        for key, value in contract.items():
            if isinstance(value, list):
                lines.append(f"{key} = {value!r}".replace("'", '"'))
            else:
                lines.append(f'{key} = "{value}"')
    return "\n".join(lines) + "\n"


def _write(root: pathlib.Path, relative: str, content: str = "") -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _build_project(root: pathlib.Path, extra: dict[str, str]) -> None:
    _write(root, "pyproject.toml", _project_contracts())
    _write(root, "app/__init__.py")
    for package in _LAYER_PACKAGES:
        _write(root, f"app/{package}/__init__.py")
    for module in MODULES:
        _write(root, f"app/modules/{module}/__init__.py")
        _write(root, f"app/modules/{module}/service.py", "")
    for relative, content in extra.items():
        _write(root, relative, content)


_LINT_IMPORTS = (
    "import sys; from importlinter.cli import lint_imports_command; "
    "sys.exit(lint_imports_command())"
)


def _run_linter(root: pathlib.Path) -> subprocess.CompletedProcess[str]:
    """Ejecuta el mismo punto de entrada que el comando `lint-imports`."""
    # S603: el ejecutable es `sys.executable` y los argumentos son constantes; no hay entrada
    # de usuario. Hace falta un subproceso porque el `app` real ya está cargado en este proceso.
    return subprocess.run(  # noqa: S603
        [sys.executable, "-c", _LINT_IMPORTS, "--config", "pyproject.toml"],
        cwd=root,
        env={"PYTHONPATH": str(root)},
        capture_output=True,
        text=True,
        check=False,
    )


def test_valid_layout_passes(tmp_path: pathlib.Path) -> None:
    _build_project(
        tmp_path,
        {
            "app/core/base.py": "VALUE = 1\n",
            "app/shared/util.py": "from app.core import base\n",
            "app/modules/auth/router.py": "from app.shared import util\n",
        },
    )

    result = _run_linter(tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr
    # Que el linter realmente evaluó los 3 contratos y los dio por cumplidos (no pasó en vacío).
    assert "Contracts: 3 kept, 0 broken" in result.stdout


@pytest.mark.parametrize(
    ("extra", "contract"),
    [
        ({"app/core/leak.py": "from app.modules.auth import router\n"}, "Direcciones"),
        ({"app/core/leak.py": "from app.shared import util\n"}, "Direcciones"),
        (
            {"app/modules/users/repository.py": "from app.modules.auth import router\n"},
            "Módulos independientes",
        ),
        ({"app/modules/auth/service.py": "import sqlalchemy\n"}, "service no accede a datos"),
        ({"app/modules/logs/service.py": "import asyncpg\n"}, "service no accede a datos"),
    ],
    ids=[
        "core_importa_modulos",
        "core_importa_shared",
        "modulo_importa_otro_modulo",
        "service_importa_sqlalchemy",
        "service_importa_asyncpg",
    ],
)
def test_forbidden_import_is_detected(
    tmp_path: pathlib.Path, extra: dict[str, str], contract: str
) -> None:
    _build_project(tmp_path, {"app/shared/util.py": "", "app/modules/auth/router.py": "", **extra})

    result = _run_linter(tmp_path)

    assert result.returncode != 0
    assert contract in result.stdout
