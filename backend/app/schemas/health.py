"""Pydantic models for the health check endpoint."""

from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response body for the health check."""

    status: Literal["ok"]
