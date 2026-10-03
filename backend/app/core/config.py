"""Configuración tipada del backend (ARQ-016).

Es el único módulo que lee `APP_ENV` y el único punto de lectura de variables de entorno.
"""

from functools import lru_cache
from typing import Annotated, Literal
from urllib.parse import urlparse

from limits import parse
from pydantic import AfterValidator, BeforeValidator, SecretStr, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

_LOCAL_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})


def _split_csv(value: object) -> object:
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return value


def _check_rate_limit(value: str) -> str:
    parse(value)
    return value


# Listas separadas por comas (sin JSON) y límites con la sintaxis de `limits`, p. ej. «10/minute».
CsvList = Annotated[list[str], NoDecode, BeforeValidator(_split_csv)]
RateLimit = Annotated[str, AfterValidator(_check_rate_limit)]


class Settings(BaseSettings):
    """Variables del grupo base del Anexo C.1; las de cada funcionalidad son opcionales hasta
    que exista el módulo que las usa."""

    # Una variable vacía cuenta como ausente: una requerida vacía impide el arranque.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_ignore_empty=True)

    app_env: Literal["development", "test", "production"]
    cors_allowed_origins: CsvList
    # Sin proxies confiables por defecto: el header de reenvío se ignora (SEC-017, falla cerrado).
    trusted_proxies: CsvList = []
    rate_limit_auth: RateLimit
    rate_limit_write: RateLimit
    rate_limit_read: RateLimit

    supabase_url: str
    supabase_secret_key: SecretStr
    database_url: SecretStr
    # Declarada sin código que la use: la conexión privilegiada nace con su primer contexto
    # declarado (DB-013).
    database_url_privileged: SecretStr

    llm_provider: str | None = None
    llm_model: str | None = None
    llm_api_key: SecretStr | None = None
    llm_max_tokens: int | None = None
    llm_timeout_seconds: int | None = None
    llm_quota_per_user: int | None = None
    llm_quota_global: int | None = None
    llm_spend_alert: int | None = None

    upload_max_bytes: int | None = None
    upload_allowed_types: CsvList = []
    upload_signed_url_ttl_seconds: int | None = None

    error_tracking_dsn: SecretStr | None = None
    notifications_provider: str | None = None
    notifications_api_key: SecretStr | None = None

    @model_validator(mode="after")
    def _validate_production(self) -> Settings:
        """SEC-019, SEC-012: en producción no se arranca con una configuración insegura."""
        if self.app_env != "production":
            return self
        problems: list[str] = []
        if "*" in self.cors_allowed_origins:
            problems.append("CORS_ALLOWED_ORIGINS no admite comodín")
        if any(urlparse(origin).hostname in _LOCAL_HOSTS for origin in self.cors_allowed_origins):
            problems.append("CORS_ALLOWED_ORIGINS no admite localhost")
        if urlparse(self.supabase_url).scheme != "https":
            problems.append("SUPABASE_URL debe usar https")
        if problems:
            raise ValueError("; ".join(problems))
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
