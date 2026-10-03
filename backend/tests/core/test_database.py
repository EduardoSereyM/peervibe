"""Contrato de sesión del usuario (B.7, DB-012, DB-014) contra Supabase local.

Pool de una sola conexión, motor propio y ejecución serializada: fuerza que todos los requests
reutilicen la misma conexión, que es donde una identidad filtrada se haría visible.
"""

import uuid
from collections.abc import AsyncIterator, Mapping

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.core import database as database_module
from app.core.config import Settings
from app.core.database import Database, SessionSetupError, create_user_engine
from app.core.errors import UnauthorizedError

USER_A = str(uuid.uuid4())
USER_B = str(uuid.uuid4())
_IDENTITY = text("SELECT current_user, auth.uid()::text, pg_backend_pid()")
_RAW_CONNECTION_STATE = text(
    "SELECT current_user, current_setting('request.jwt.claims', true), pg_backend_pid()"
)


def _claims(subject: str, **extra: object) -> dict[str, object]:
    return {"sub": subject, "role": "authenticated", "aal": "aal1", **extra}


async def _identity(session: AsyncSession) -> tuple[str, str | None, int]:
    row = (await session.execute(_IDENTITY)).one()
    return row[0], row[1], row[2]


@pytest.fixture
async def engine() -> AsyncIterator[AsyncEngine]:
    local = create_user_engine(Settings(), pool_size=1, max_overflow=0)
    yield local
    await local.dispose()


@pytest.fixture
def database(engine: AsyncEngine) -> Database:
    return Database(engine)


@pytest.mark.integration
async def test_identity_is_not_shared_between_requests_on_the_same_connection(
    database: Database, engine: AsyncEngine
) -> None:
    async with database.user_session(_claims(USER_A)) as session:
        role_a, uid_a, pid_a = await _identity(session)
    async with database.user_session(_claims(USER_B)) as session:
        role_b, uid_b, pid_b = await _identity(session)
    async with database.anonymous_session() as session:
        role_anon, uid_anon, pid_anon = await _identity(session)

    assert pid_a == pid_b == pid_anon
    assert (role_a, uid_a) == ("authenticated", USER_A)
    assert (role_b, uid_b) == ("authenticated", USER_B)
    assert (role_anon, uid_anon) == ("anon", None)
    async with engine.connect() as connection:
        role, claims, pid = (await connection.execute(_RAW_CONNECTION_STATE)).one()
    assert pid == pid_a
    assert role not in {"authenticated", "anon"}
    assert not claims


@pytest.mark.integration
async def test_all_verified_claims_are_available_to_policies(database: Database) -> None:
    async with database.user_session(_claims(USER_A, aal="aal2")) as session:
        aal = (await session.execute(text("SELECT auth.jwt() ->> 'aal'"))).scalar_one()
        subject = (await session.execute(text("SELECT auth.jwt() ->> 'sub'"))).scalar_one()

    assert (aal, subject) == ("aal2", USER_A)


@pytest.mark.integration
async def test_malicious_claim_values_do_not_alter_the_session(database: Database) -> None:
    hostile = "x'; SET LOCAL ROLE postgres; --"
    async with database.user_session(_claims(USER_A, email=hostile)) as session:
        role, uid, _ = await _identity(session)
        email = (await session.execute(text("SELECT auth.jwt() ->> 'email'"))).scalar_one()

    assert (role, uid, email) == ("authenticated", USER_A, hostile)


@pytest.mark.integration
async def test_anonymous_session_has_role_anon_and_no_claims(database: Database) -> None:
    async with database.anonymous_session() as session:
        role, uid, _ = await _identity(session)
        claims = (
            await session.execute(text("SELECT current_setting('request.jwt.claims', true)"))
        ).scalar_one()

    assert role == "anon"
    assert uid is None
    assert not claims


@pytest.mark.integration
@pytest.mark.parametrize(
    ("constant", "replacement"),
    [
        ("_SET_ROLE_ANONYMOUS", "SET LOCAL ROLE rol_que_no_existe"),
        ("_SET_ROLE_ANONYMOUS", "SET LOCAL ROLE authenticated"),
        ("_READ_IDENTITY", "SELECT 'anon', gen_random_uuid()::text"),
    ],
    ids=["falla_al_fijar_el_rol", "rol_efectivo_distinto", "claims_inesperados"],
)
async def test_anonymous_session_failure_aborts_the_request(
    monkeypatch: pytest.MonkeyPatch, database: Database, constant: str, replacement: str
) -> None:
    with monkeypatch.context() as patch:
        patch.setattr(database_module, constant, text(replacement))
        with pytest.raises(SessionSetupError) as error:
            async with database.anonymous_session():
                pytest.fail("no debe ejecutarse ninguna query con una identidad dudosa")

    assert error.value.status_code == 500
    async with database.anonymous_session() as session:
        role, uid, _ = await _identity(session)
    assert (role, uid) == ("anon", None)


@pytest.mark.integration
@pytest.mark.parametrize(
    "replacement",
    ["SET LOCAL ROLE rol_que_no_existe", "SET LOCAL ROLE anon"],
    ids=["falla_al_fijar_el_rol", "rol_efectivo_distinto"],
)
async def test_role_failure_aborts_the_request_and_leaves_the_connection_usable(
    monkeypatch: pytest.MonkeyPatch, database: Database, replacement: str
) -> None:
    with monkeypatch.context() as patch:
        patch.setattr(database_module, "_SET_ROLE_AUTHENTICATED", text(replacement))
        with pytest.raises(SessionSetupError) as error:
            async with database.user_session(_claims(USER_A)):
                pytest.fail("no debe ejecutarse ninguna query sin identidad")

    assert error.value.status_code == 500
    async with database.user_session(_claims(USER_B)) as session:
        role, uid, _ = await _identity(session)
    assert (role, uid) == ("authenticated", USER_B)


@pytest.mark.integration
async def test_body_error_rolls_back_and_clears_identity(database: Database) -> None:
    with pytest.raises(ZeroDivisionError):
        async with database.user_session(_claims(USER_A)):
            raise ZeroDivisionError

    async with database.anonymous_session() as session:
        _, uid, _ = await _identity(session)
    assert uid is None


@pytest.mark.parametrize(
    "claims",
    [
        {"role": "authenticated"},
        {"sub": "", "role": "authenticated"},
        {"sub": "no-es-uuid", "role": "authenticated"},
        {"sub": 123, "role": "authenticated"},
        {"sub": USER_A, "role": "service_role"},
        {"sub": USER_A, "role": "anon"},
        {"sub": USER_A},
    ],
    ids=["sin_sub", "sub_vacio", "sub_no_uuid", "sub_no_texto", "service_role", "anon", "sin_rol"],
)
async def test_invalid_claims_are_rejected_with_401_before_touching_the_database(
    closed_database: Database, claims: Mapping[str, object]
) -> None:
    # La base de datos es inalcanzable: si se intentara conectar, el error sería otro.
    with pytest.raises(UnauthorizedError) as error:
        async with closed_database.user_session(claims):
            pytest.fail("no debe abrirse la sesión")

    assert error.value.status_code == 401
