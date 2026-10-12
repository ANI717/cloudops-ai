"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api.main import api_router
from app.core.config import APP_VERSION, Settings, get_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build and configure the FastAPI application."""
    settings = settings or get_settings()

    # Interactive API docs are disabled in production to reduce exposed surface.
    docs_enabled = not settings.is_production

    app = FastAPI(
        title=settings.app_name,
        version=APP_VERSION,
        docs_url="/docs" if docs_enabled else None,
        redoc_url="/redoc" if docs_enabled else None,
        openapi_url="/openapi.json" if docs_enabled else None,
    )
    app.include_router(api_router)
    return app


app = create_app()
