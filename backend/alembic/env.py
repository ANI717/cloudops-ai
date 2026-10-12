"""Alembic migration environment.

The database URL comes from app settings (CLOUDOPS_POSTGRES_* env vars or
backend/.env), never from a config file. Callers such as the test suite can
instead pass an open connection via ``config.attributes["connection"]``.
"""

from logging.config import fileConfig

from sqlalchemy import Connection, create_engine, pool

from alembic import context
from app.core.config import get_settings
from app.models import Base

config = context.config

# Only configure logging when run from the CLI, so we don't override the
# logging setup of a host process (e.g. pytest) that runs migrations.
if config.config_file_name is not None and "connection" not in config.attributes:
    fileConfig(config.config_file_name)

# Autogenerate compares the database against these models.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Emit migration SQL to stdout (`alembic upgrade head --sql`), no DB needed."""
    context.configure(
        url=get_settings().database_url.render_as_string(hide_password=False),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations against a live database."""
    connection = config.attributes.get("connection")
    if connection is not None:
        do_run_migrations(connection)
        return

    engine = create_engine(get_settings().database_url, poolclass=pool.NullPool)
    with engine.connect() as connection:
        do_run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
