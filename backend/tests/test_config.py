import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.core.config import Settings
from app.main import create_app


def make_settings(**overrides: str) -> Settings:
    # _env_file=None ignores any local .env so results don't depend on the machine.
    return Settings(_env_file=None, **overrides)  # type: ignore[arg-type]


def test_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CLOUDOPS_ENVIRONMENT", raising=False)
    monkeypatch.delenv("CLOUDOPS_APP_NAME", raising=False)

    settings = make_settings()

    assert settings.app_name == "CloudOps AI"
    assert settings.environment == "development"
    assert settings.is_production is False


def test_environment_variable_overrides_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CLOUDOPS_ENVIRONMENT", "production")
    monkeypatch.setenv("CLOUDOPS_APP_NAME", "CloudOps Staging")

    settings = make_settings()

    assert settings.environment == "production"
    assert settings.app_name == "CloudOps Staging"
    assert settings.is_production is True


def test_invalid_environment_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CLOUDOPS_ENVIRONMENT", "bogus")

    with pytest.raises(ValidationError):
        make_settings()


def test_docs_available_outside_production() -> None:
    client = TestClient(create_app(make_settings(environment="development")))

    assert client.get("/docs").status_code == 200
    assert client.get("/openapi.json").status_code == 200


def test_docs_disabled_in_production() -> None:
    client = TestClient(create_app(make_settings(environment="production")))

    assert client.get("/docs").status_code == 404
    assert client.get("/redoc").status_code == 404
    assert client.get("/openapi.json").status_code == 404
    assert client.get("/health").status_code == 200
