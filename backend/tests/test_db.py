from fastapi.testclient import TestClient
from sqlalchemy import Engine, event, inspect, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import get_settings
from app.core.db import CONNECT_TIMEOUT_SECONDS, get_engine
from app.main import create_app
from tests.db import rolled_back_session


def test_tests_use_the_test_database(db_session: Session) -> None:
    current = db_session.execute(text("SELECT current_database()")).scalar_one()

    assert current == get_settings().postgres_db
    assert current.endswith("_test")


def test_migrations_applied(engine: Engine) -> None:
    assert "alembic_version" in inspect(engine).get_table_names()


def test_get_db_yields_working_session(engine: Engine) -> None:
    dependency = get_db()
    session = next(dependency)

    assert session.execute(text("SELECT 1")).scalar_one() == 1
    dependency.close()  # runs the dependency's cleanup, closing the session


def test_engine_fails_fast_when_database_unreachable() -> None:
    # Guards against requests hanging for minutes during a database outage.
    engine = get_engine()
    captured: dict[str, object] = {}

    def capture(_d: object, _r: object, _a: object, params: dict[str, object]) -> None:
        captured.update(params)

    engine.dispose()  # force a brand-new connection so the event fires
    event.listen(engine, "do_connect", capture)
    try:
        with engine.connect():
            pass
    finally:
        event.remove(engine, "do_connect", capture)

    assert captured["connect_timeout"] == CONNECT_TIMEOUT_SECONDS


def test_session_changes_are_rolled_back(engine: Engine) -> None:
    with rolled_back_session(engine) as session:
        session.execute(text("CREATE TABLE rollback_probe (id int)"))
        session.execute(text("INSERT INTO rollback_probe VALUES (1)"))
        session.commit()  # becomes a savepoint; the outer transaction still rolls back

    assert "rollback_probe" not in inspect(engine).get_table_names()


def test_ready_when_database_reachable(client: TestClient) -> None:
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


class _UnreachableDatabase:
    def execute(self, *args: object, **kwargs: object) -> None:
        raise OperationalError("SELECT 1", {}, Exception("connection refused"))


def test_ready_returns_503_when_database_unreachable() -> None:
    app = create_app()
    app.dependency_overrides[get_db] = lambda: _UnreachableDatabase()
    client = TestClient(app)

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}
    # Liveness is independent of the database.
    assert client.get("/health").status_code == 200
