"""Database engine and session factory.

The engine is created lazily on first use, so importing the app (or running
tests that never touch the database) doesn't require a running PostgreSQL.
"""

from functools import lru_cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

# Fail fast when the database is unreachable. Without this, psycopg can wait
# minutes per connection attempt, hanging requests and readiness probes.
CONNECT_TIMEOUT_SECONDS = 3


@lru_cache
def get_engine() -> Engine:
    """Return the process-wide engine (it holds the connection pool)."""
    # pool_pre_ping checks a pooled connection before use, replacing dead ones
    # (e.g. after a database restart) instead of failing the request.
    return create_engine(
        get_settings().database_url,
        pool_pre_ping=True,
        connect_args={"connect_timeout": CONNECT_TIMEOUT_SECONDS},
    )


@lru_cache
def get_session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=get_engine(), autoflush=False, expire_on_commit=False)
