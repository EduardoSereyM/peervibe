import pathlib
import re
from collections.abc import Callable

import pytest
from pydantic import ValidationError

from app.core.config import Settings
from tests.conftest import VALID_ENV

APP_DIR = pathlib.Path(__file__).resolve().parents[2] / "app"
REQUIRED = [
    "APP_ENV",
    "CORS_ALLOWED_ORIGINS",
    "RATE_LIMIT_AUTH",
    "RATE_LIMIT_WRITE",
    "RATE_LIMIT_READ",
    "SUPABASE_URL",
    "SUPABASE_SECRET_KEY",
    "DATABASE_URL",
    "DATABASE_URL_PRIVILEGED",
]


def test_valid_configuration_loads(make_settings: Callable[..., Settings]) -> None:
    settings = make_settings()

    assert settings.cors_allowed_origins == ["http://localhost:5173"]
    assert settings.trusted_proxies == []
    assert settings.llm_api_key is None
    assert "sb_secret_sintetica" not in repr(settings)


@pytest.mark.parametrize("name", REQUIRED)
def test_missing_required_variable_fails(clean_env: pytest.MonkeyPatch, name: str) -> None:
    clean_env.delenv(name)

    with pytest.raises(ValidationError) as error:
        Settings(_env_file=None)

    assert name.lower() in str(error.value)


def test_empty_required_variable_fails(clean_env: pytest.MonkeyPatch) -> None:
    clean_env.setenv("DATABASE_URL", "")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_invalid_rate_limit_fails(make_settings: Callable[..., Settings]) -> None:
    with pytest.raises(ValidationError):
        make_settings(RATE_LIMIT_AUTH="muchas por segundo")


@pytest.mark.parametrize(
    "overrides",
    [
        {"CORS_ALLOWED_ORIGINS": "*"},
        {"CORS_ALLOWED_ORIGINS": "https://peervibe.cl,http://localhost:5173"},
        {"SUPABASE_URL": "http://proyecto.supabase.co"},
    ],
)
def test_insecure_production_configuration_fails(
    make_settings: Callable[..., Settings], overrides: dict[str, str]
) -> None:
    base = {"CORS_ALLOWED_ORIGINS": "https://peervibe.cl", "SUPABASE_URL": "https://p.supabase.co"}

    with pytest.raises(ValidationError):
        make_settings(APP_ENV="production", **(base | overrides))


def test_secure_production_configuration_loads(make_settings: Callable[..., Settings]) -> None:
    settings = make_settings(
        APP_ENV="production",
        CORS_ALLOWED_ORIGINS="https://peervibe.cl",
        SUPABASE_URL="https://p.supabase.co",
    )

    assert settings.app_env == "production"


def test_unknown_environment_fails(make_settings: Callable[..., Settings]) -> None:
    with pytest.raises(ValidationError):
        make_settings(APP_ENV="staging-raro")


def test_app_env_is_read_only_in_config_module() -> None:
    """OPS-002: el nombre del entorno solo se consulta en `core/config.py`."""
    offenders = [
        path.relative_to(APP_DIR).as_posix()
        for path in APP_DIR.rglob("*.py")
        if path.name != "config.py" and re.search(r"app_env", path.read_text(), re.IGNORECASE)
    ]

    assert offenders == []


def test_valid_env_covers_all_required_variables() -> None:
    assert set(REQUIRED) <= set(VALID_ENV)
