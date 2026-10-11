"""Health check endpoint used by load balancers, Kubernetes probes, and monitoring."""

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Response body for the health check."""

    status: Literal["ok"]


@router.get("/health")
def health() -> HealthResponse:
    """Report that the service process is running and able to handle requests."""
    return HealthResponse(status="ok")
