"""Conexión que opera como el usuario (DB-012, DB-014, contrato B.7).

Solo existe el motor del usuario y el modo anónimo: la conexión privilegiada (DB-013) nace con
su primer contexto declarado. Todo el SQL son constantes; los valores viajan como parámetros
ligados (SEC-013) y los roles son literales fijos, porque `SET LOCAL ROLE` no admite parámetros.
"""

import asyncio
import json
import uuid
from collections.abc import AsyncIterator, Mapping
from contextlib import asynccontextmanager

from fastapi import Request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import Settings
from app.core.errors import AppError, ServiceUnavailableError, UnauthorizedError

AUTHENTICATED_ROLE = "authenticated"
ANONYMOUS_ROLE = "anon"
_DEFAULT_POOL_SIZE = 5
_DEFAULT_MAX_OVERFLOW = 10
_PING_TIMEOUT_SECONDS = 2

_SET_CLAIMS = text("SELECT set_config('request.jwt.claims', :claims, true)")
_SET_ROLE_AUTHENTICATED = text("SET LOCAL ROLE authenticated")
_SET_ROLE_ANONYMOUS = text("SET LOCAL ROLE anon")
_READ_IDENTITY = text("SELECT current_user, auth.uid()::text")
_PING = text("SELECT 1")


class SessionSetupError(AppError):
    """No se pudo fijar la identidad de la sesión: el request se aborta, nunca corre sin
    identidad."""


def _verified_subject(claims: Mapping[str, object]) -> str:
    """El `sub` del token como UUID canónico; sin él, o con otro rol, no se abre sesión."""
    subject = claims.get("sub")
    if claims.get("role") != AUTHENTICATED_ROLE or not isinstance(subject, str):
        raise UnauthorizedError
    try:
        return str(uuid.UUID(subject))
    except ValueError as exc:
        raise UnauthorizedError from exc


async def _read_identity(session: AsyncSession) -> tuple[str, str | None]:
    row = (await session.execute(_READ_IDENTITY)).one()
    return row[0], row[1]


def create_user_engine(
    settings: Settings,
    *,
    pool_size: int = _DEFAULT_POOL_SIZE,
    max_overflow: int = _DEFAULT_MAX_OVERFLOW,
) -> AsyncEngine:
    """Motor del rol de conexión que cambia al usuario (B.7.5), apto para pooler en modo
    transacción: sin caché de sentencias preparadas y con nombres de sentencia únicos (B.7.6)."""
    return create_async_engine(
        settings.database_url.get_secret_value(),
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_pre_ping=True,
        connect_args={
            "statement_cache_size": 0,
            "prepared_statement_cache_size": 0,
            "prepared_statement_name_func": lambda: "__asyncpg_" + uuid.uuid4().hex + "__",
        },
    )


class Database:
    """Abre una sesión nueva por llamada, dentro de una transacción; nunca cachea ni comparte."""

    def __init__(self, engine: AsyncEngine) -> None:
        self._engine = engine
        self._sessions = async_sessionmaker(engine, expire_on_commit=False)

    @asynccontextmanager
    async def user_session(self, claims: Mapping[str, object]) -> AsyncIterator[AsyncSession]:
        """Sesión como el usuario: claims verificados (SEC-001), nunca el token crudo."""
        subject = _verified_subject(claims)
        async with self._sessions() as session, session.begin():
            try:
                await session.execute(_SET_CLAIMS, {"claims": json.dumps(dict(claims))})
                await session.execute(_SET_ROLE_AUTHENTICATED)
                role, uid = await _read_identity(session)
            except (SQLAlchemyError, OSError) as exc:
                raise SessionSetupError from exc
            if role != AUTHENTICATED_ROLE or uid != subject:
                raise SessionSetupError
            yield session

    @asynccontextmanager
    async def anonymous_session(self) -> AsyncIterator[AsyncSession]:
        """Modo anónimo explícito (SEC-003): rol `anon` y sin claims."""
        async with self._sessions() as session, session.begin():
            try:
                await session.execute(_SET_ROLE_ANONYMOUS)
                role, uid = await _read_identity(session)
            except (SQLAlchemyError, OSError) as exc:
                raise SessionSetupError from exc
            if role != ANONYMOUS_ROLE or uid is not None:
                raise SessionSetupError
            yield session

    async def ping(self) -> None:
        """Comprueba que la base de datos responde (OPS-004)."""
        try:
            async with asyncio.timeout(_PING_TIMEOUT_SECONDS), self._engine.connect() as connection:
                await connection.execute(_PING)
        except (SQLAlchemyError, OSError, TimeoutError) as exc:
            raise ServiceUnavailableError from exc

    async def dispose(self) -> None:
        await self._engine.dispose()


def get_database(request: Request) -> Database:
    database = request.app.state.database
    if not isinstance(database, Database):
        raise ServiceUnavailableError
    return database
