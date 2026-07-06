from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ActivityLogResponse(BaseModel):
    id: UUID
    timestamp: str
    sensor_id: Optional[UUID] = None
    action: str
    provider: Optional[str] = None
    description: Optional[str] = None
    severity: str = Field(..., example="INFO")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "00000000-0000-0000-0000-000000000001",
                "timestamp": "2026-07-06T12:00:00Z",
                "sensor_id": "00000000-0000-0000-0000-000000000002",
                "action": "sensor.registered",
                "provider": "esp32",
                "description": "Sensor registered through discovery.",
                "severity": "INFO",
            }
        },
    )
