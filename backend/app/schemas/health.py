from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response schema for health check endpoints."""

    status: str
