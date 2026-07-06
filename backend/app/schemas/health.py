from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """Response schema for health check endpoints."""

    status: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "OK",
            }
        }
    )
