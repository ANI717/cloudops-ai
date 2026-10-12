"""Application-wide configuration.

Settings are read from environment variables prefixed with ``CLOUDOPS_``
(e.g. ``CLOUDOPS_ENVIRONMENT=production``), falling back to a ``.env`` file in
the working directory, then to the defaults below. See ``backend/.env.example``.
"""

from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

# Describes the code, not the deployment, so it is not configurable.
APP_VERSION = "0.1.0"

Environment = Literal["development", "test", "production"]


class Settings(BaseSettings):
    """Runtime settings, validated at startup."""

    model_config = SettingsConfigDict(
        env_prefix="CLOUDOPS_",
        env_file=".env",
        extra="ignore",
    )

    app_name: str = "CloudOps AI"
    environment: Environment = "development"

    postgres_host: str = "127.0.0.1"
    postgres_port: int = 5432
    postgres_user: str = "cloudops"
    # Required, no default: credentials must always come from the environment.
    postgres_password: SecretStr
    postgres_db: str = "cloudops"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def database_url(self) -> URL:
        """SQLAlchemy URL; URL.create escapes special characters in the password."""
        return URL.create(
            drivername="postgresql+psycopg",
            username=self.postgres_user,
            password=self.postgres_password.get_secret_value(),
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        )


@lru_cache
def get_settings() -> Settings:
    """Return the settings, loaded once per process."""
    return Settings()  # required fields (e.g. the password) come from env / .env
