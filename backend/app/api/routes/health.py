"""Health check endpoint used by load balancers, Kubernetes probes, and monitoring."""

from fastapi import APIRouter

from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> HealthResponse:
    """Report that the service process is running and able to handle requests."""
    return HealthResponse(status="ok")
