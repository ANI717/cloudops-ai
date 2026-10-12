"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api.main import api_router
from app.core.config import APP_TITLE, APP_VERSION


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    app = FastAPI(title=APP_TITLE, version=APP_VERSION)
    app.include_router(api_router)
    return app


app = create_app()
