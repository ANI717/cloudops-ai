"""Test database helpers (no side effects on import; fixtures live in conftest.py)."""

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from alembic.config import Config
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session

from alembic import command
from app.core.config import Settings

TEST_DB_SUFFIX = "_test"
BACKEND_DIR = Path(__file__).resolve().parent.parent


def create_database_if_missing(settings: Settings) -> None:
    # CREATE DATABASE can't run inside a transaction, hence AUTOCOMMIT, and it
    # must be issued from another database (the default "postgres" one).
    admin_url = settings.database_url.set(database="postgres")
    admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
    try:
        with admin_engine.connect() as conn:
            exists = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :name"),
                {"name": settings.postgres_db},
            ).scalar()
            if not exists:
                quoted = conn.dialect.identifier_preparer.quote(settings.postgres_db)
                conn.execute(text(f"CREATE DATABASE {quoted}"))
    finally:
        admin_engine.dispose()


def migrate_from_scratch(engine: Engine) -> None:
    config = Config(
        file_=BACKEND_DIR / "alembic.ini", toml_file=BACKEND_DIR / "pyproject.toml"
    )
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        config.attributes["connection"] = conn
        command.upgrade(config, "head")


@contextmanager
def rolled_back_session(engine: Engine) -> Iterator[Session]:
    """A session whose work, including commits, is undone on exit.

    The outer transaction is never committed. ``create_savepoint`` turns any
    ``session.commit()`` in the code under test into a savepoint inside it.
    """
    with engine.connect() as connection:
        transaction = connection.begin()
        session = Session(bind=connection, join_transaction_mode="create_savepoint")
        try:
            yield session
        finally:
            session.close()
            transaction.rollback()
