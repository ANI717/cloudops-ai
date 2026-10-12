"""Application-wide configuration.

Settings are read from environment variables prefixed with ``CLOUDOPS_``
(e.g. ``CLOUDOPS_ENVIRONMENT=production``), falling back to a ``.env`` file in
the working directory, then to the defaults below. See ``backend/.env.example``.
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

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

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    """Return the settings, loaded once per process."""
    return Settings()
