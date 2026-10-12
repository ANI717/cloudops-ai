"""Pydantic models for the health and readiness endpoints."""

from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response body for the health check."""

    status: Literal["ok"]


class ReadyResponse(BaseModel):
    """Response body for the readiness check."""

    status: Literal["ready"]
