import ast
import pathlib

APP_DIR = pathlib.Path(__file__).resolve().parents[2] / "app"


def _sources() -> list[tuple[pathlib.Path, ast.Module]]:
    return [(path, ast.parse(path.read_text())) for path in APP_DIR.rglob("*.py")]


def test_every_sql_text_is_a_constant_string() -> None:
    """SEC-013: nada se interpola ni concatena en SQL; los valores van como parámetros."""
    offenders = []
    for path, tree in _sources():
        for node in ast.walk(tree):
            if not (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "text"
            ):
                continue
            argument = node.args[0] if len(node.args) == 1 else None
            if not (isinstance(argument, ast.Constant) and isinstance(argument.value, str)):
                offenders.append(f"{path.relative_to(APP_DIR)}:{node.lineno}")

    assert offenders == []


def test_database_module_builds_no_strings_dynamically() -> None:
    tree = ast.parse((APP_DIR / "core" / "database.py").read_text())

    fstrings = [node.lineno for node in ast.walk(tree) if isinstance(node, ast.JoinedStr)]

    assert fstrings == []


def test_privileged_connection_is_declared_but_unused() -> None:
    """DB-013: la conexión privilegiada nace con su primer contexto declarado."""
    users = [
        path.relative_to(APP_DIR).as_posix()
        for path, _ in _sources()
        if path.name != "config.py" and "database_url_privileged" in path.read_text().lower()
    ]

    assert users == []


def test_asyncpg_prepared_statements_are_disabled() -> None:
    """B.7.6: pooler en modo transacción, sin sentencias preparadas persistentes."""
    source = (APP_DIR / "core" / "database.py").read_text()

    assert '"statement_cache_size": 0' in source
    assert '"prepared_statement_cache_size": 0' in source
