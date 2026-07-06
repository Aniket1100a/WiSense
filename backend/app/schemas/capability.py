from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic import ConfigDict


class CapabilityBase(BaseModel):
    capability_name: str = Field(..., max_length=200)
    description: Optional[str] = None
    enabled: Optional[bool] = True

    model_config = ConfigDict(from_attributes=True)


class CapabilityCreate(CapabilityBase):
    sensor_id: UUID

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "capability_name": "temperature",
                "description": "Provides ambient temperature readings.",
                "enabled": True,
                "sensor_id": "00000000-0000-0000-0000-000000000000",
            }
        },
    )


class CapabilityUpdate(BaseModel):
    capability_name: Optional[str] = None
    description: Optional[str] = None
    enabled: Optional[bool] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "enabled": False,
                "description": "Disable this capability temporarily.",
            }
        },
    )


class CapabilityResponse(CapabilityBase):
    id: UUID
    sensor_id: UUID
    created_at: Optional[str]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "00000000-0000-0000-0000-000000000001",
                "capability_name": "temperature",
                "description": "Provides ambient temperature readings.",
                "enabled": True,
                "sensor_id": "00000000-0000-0000-0000-000000000000",
                "created_at": "2026-07-06T12:00:00Z",
            }
        },
    )
