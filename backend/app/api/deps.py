"""Shared FastAPI dependencies for route handlers."""

from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.db import get_session_factory


def get_db() -> Generator[Session]:
    """Provide a database session for one request, always closing it afterwards."""
    with get_session_factory()() as session:
        yield session


DbSession = Annotated[Session, Depends(get_db)]
