"""Health and readiness endpoints for load balancers, Kubernetes probes, and monitoring.

- ``/health`` (liveness): the process is up. It never checks dependencies, so a
  database outage doesn't get healthy app instances restarted.
- ``/ready`` (readiness): the app can serve real traffic, i.e. the database is
  reachable. Returns 503 otherwise, so traffic is routed elsewhere.
"""

import logging

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import DbSession
from app.schemas.health import HealthResponse, ReadyResponse

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> HealthResponse:
    """Report that the service process is running and able to handle requests."""
    return HealthResponse(status="ok")


@router.get(
    "/ready",
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "Database unavailable"}
    },
)
def ready(db: DbSession) -> ReadyResponse:
    """Report whether the service can reach its database."""
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        # Log details server-side; don't leak connection info to the client.
        logger.warning("Readiness check failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        ) from exc
    return ReadyResponse(status="ready")
