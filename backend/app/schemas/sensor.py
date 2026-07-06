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

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "lab-temperaturesensor",
                "description": "ESP32 temperature sensor in the lab",
                "provider": "esp32",
                "sensor_type": "TEMPERATURE",
                "status": "OFFLINE",
                "firmware_version": "1.0.0",
                "hardware_version": "A1",
                "serial_number": "ESP32-0001",
                "mac_address": "aa:bb:cc:11:22:33",
                "ip_address": "192.168.1.100",
                "location": "lab-1",
                "room_id": "00000000-0000-0000-0000-000000000000",
                "is_active": True,
                "meta": {"manufacturer": "ExampleCo"},
            }
        },
    )


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

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "lab-sensor-updated",
                "status": "ONLINE",
                "location": "lab-1",
                "meta": {"notes": "Updated via API"},
            }
        },
    )


class SensorResponse(SensorBase):
    id: UUID
    created_at: Optional[str]
    updated_at: Optional[str]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "00000000-0000-0000-0000-000000000001",
                "name": "lab-temperaturesensor",
                "description": "ESP32 temperature sensor in the lab",
                "provider": "esp32",
                "sensor_type": "TEMPERATURE",
                "status": "ONLINE",
                "firmware_version": "1.0.0",
                "hardware_version": "A1",
                "serial_number": "ESP32-0001",
                "mac_address": "aa:bb:cc:11:22:33",
                "ip_address": "192.168.1.100",
                "location": "lab-1",
                "room_id": "00000000-0000-0000-0000-000000000000",
                "is_active": True,
                "meta": {"manufacturer": "ExampleCo"},
                "created_at": "2026-07-06T12:00:00Z",
                "updated_at": "2026-07-06T12:00:00Z",
            }
        },
    )
