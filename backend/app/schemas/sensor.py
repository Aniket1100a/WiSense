from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic import ConfigDict

from app.models.sensor import ProviderEnum, SensorTypeEnum, SensorStatusEnum


class SensorBase(BaseModel):
    """Base schema shared by create and update operations."""

    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    provider: ProviderEnum
    sensor_type: SensorTypeEnum
    status: Optional[SensorStatusEnum] = SensorStatusEnum.offline
    firmware_version: Optional[str] = None
    hardware_version: Optional[str] = None
    serial_number: Optional[str] = None
    mac_address: Optional[str] = None
    ip_address: Optional[str] = None
    location: Optional[str] = None
    room_id: Optional[UUID] = None
    is_active: Optional[bool] = True
    meta: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)


class SensorCreate(SensorBase):
    """Schema for creating a sensor."""


class SensorUpdate(BaseModel):
    """Schema for updating a sensor."""

    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[SensorStatusEnum] = None
    firmware_version: Optional[str] = None
    hardware_version: Optional[str] = None
    serial_number: Optional[str] = None
    mac_address: Optional[str] = None
    ip_address: Optional[str] = None
    location: Optional[str] = None
    room_id: Optional[UUID] = None
    is_active: Optional[bool] = None
    meta: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)


class SensorResponse(SensorBase):
    id: UUID
    created_at: Optional[str]
    updated_at: Optional[str]

    model_config = ConfigDict(from_attributes=True)
