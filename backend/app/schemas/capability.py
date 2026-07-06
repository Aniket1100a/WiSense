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


class CapabilityUpdate(BaseModel):
    capability_name: Optional[str] = None
    description: Optional[str] = None
    enabled: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class CapabilityResponse(CapabilityBase):
    id: UUID
    sensor_id: UUID
    created_at: Optional[str]

    model_config = ConfigDict(from_attributes=True)
