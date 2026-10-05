"""Exportación del OpenAPI (ARQ-010): el archivo commiteado es el que genera la aplicación.

Todo lo que escriben estos tests va a `tmp_path`; el único archivo del repositorio que se toca es
`backend/openapi.json`, y solo para leerlo.
"""

import pathlib
import runpy
import sys

import pytest

from app.export_openapi import REGENERATE_COMMAND, main, render_openapi

COMMITTED = pathlib.Path(__file__).resolve().parents[1] / "openapi.json"
MODULE = "app.export_openapi"


def _committed_copy(tmp_path: pathlib.Path) -> pathlib.Path:
    copy = tmp_path / "copia.json"
    copy.write_bytes(COMMITTED.read_bytes())
    return copy


def test_committed_openapi_matches_the_application() -> None:
    assert COMMITTED.read_text(encoding="utf-8") == render_openapi(), (
        f"backend/openapi.json no coincide con la aplicación: ejecuta `{REGENERATE_COMMAND}`"
    )


def test_regenerate_command_points_to_the_client_generation_script() -> None:
    assert REGENERATE_COMMAND == "npm run generate:client"


def test_write_is_identical_to_the_committed_file_and_deterministic(
    tmp_path: pathlib.Path,
) -> None:
    first = tmp_path / "primera.json"
    second = tmp_path / "segunda.json"

    assert main([str(first)]) == 0
    assert main([str(second)]) == 0

    assert first.read_bytes() == second.read_bytes() == COMMITTED.read_bytes()


def test_check_returns_0_on_the_correct_file_without_writing(tmp_path: pathlib.Path) -> None:
    copy = _committed_copy(tmp_path)
    before = copy.stat().st_mtime_ns

    assert main([str(copy), "--check"]) == 0

    assert copy.read_bytes() == COMMITTED.read_bytes()
    assert copy.stat().st_mtime_ns == before


def test_check_returns_1_on_an_altered_copy_and_leaves_it_untouched(
    tmp_path: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    copy = _committed_copy(tmp_path)
    altered = copy.read_text(encoding="utf-8").replace('"health"', '"salud"', 1)
    copy.write_text(altered, encoding="utf-8")

    assert main([str(copy), "--check"]) == 1

    assert copy.read_text(encoding="utf-8") == altered
    assert REGENERATE_COMMAND in capsys.readouterr().err


def test_check_returns_1_when_the_file_does_not_exist(
    tmp_path: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "no-existe.json"

    assert main([str(missing), "--check"]) == 1

    assert not missing.exists()
    assert REGENERATE_COMMAND in capsys.readouterr().err


def test_running_the_module_as_a_script_writes_the_file(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output = tmp_path / "script.json"
    monkeypatch.setattr(sys, "argv", [MODULE, str(output)])
    # `runpy` avisa si el módulo ya está importado; se quita para ejecutarlo como `__main__`.
    monkeypatch.delitem(sys.modules, MODULE)

    with pytest.raises(SystemExit) as exit_info:
        runpy.run_module(MODULE, run_name="__main__")

    assert exit_info.value.code == 0
    assert output.read_bytes() == COMMITTED.read_bytes()
