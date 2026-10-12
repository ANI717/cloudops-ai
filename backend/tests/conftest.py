"""Shared test fixtures.

Database tests run against a real PostgreSQL test database, never mocks, so SQL,
constraints, and migrations are exercised for real:

- The test database is "<CLOUDOPS_POSTGRES_DB>_test" (e.g. ``cloudops_test``),
  so tests never touch development data. It is created if missing.
- Each test session rebuilds the schema from scratch with Alembic migrations.
- Each test runs inside a transaction that is rolled back afterwards.

Tests that don't request a database fixture never open a connection.
"""

import os
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from tests.db import (
    TEST_DB_SUFFIX,
    create_database_if_missing,
    migrate_from_scratch,
    rolled_back_session,
)

# Point the whole app at the test database before anything reads settings.
_db_name = Settings().postgres_db
if not _db_name.endswith(TEST_DB_SUFFIX):
    os.environ["CLOUDOPS_POSTGRES_DB"] = f"{_db_name}{TEST_DB_SUFFIX}"
os.environ["CLOUDOPS_ENVIRONMENT"] = "test"
get_settings.cache_clear()


@pytest.fixture(scope="session")
def engine() -> Iterator[Engine]:
    """Engine for the migrated test database, shared by the whole test session."""
    settings = get_settings()
    assert settings.postgres_db.endswith(TEST_DB_SUFFIX), "refusing non-test database"
    create_database_if_missing(settings)
    engine = create_engine(settings.database_url)
    migrate_from_scratch(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(engine: Engine) -> Iterator[Session]:
    """A database session for one test; everything it does is rolled back."""
    with rolled_back_session(engine) as session:
        yield session


@pytest.fixture
def client(db_session: Session) -> Iterator[TestClient]:
    """Test client whose requests use the test's rolled-back session."""
    from app.api.deps import get_db
    from app.main import create_app

    app = create_app()
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as test_client:
        yield test_client
