from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic import ConfigDict

from app.models.sensor import ProviderEnum, SensorStatusEnum


class SensorRegister(BaseModel):
    name: str = Field(..., max_length=200)
    provider: ProviderEnum
    serial_number: Optional[str] = None
    mac_address: Optional[str] = None
    firmware_version: Optional[str] = None
    hardware_version: Optional[str] = None
    serial: Optional[str] = None
    ip_address: Optional[str] = None
    location: Optional[str] = None
    room_id: Optional[UUID] = None
    meta: Optional[dict] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "lobby-sensor",
                "provider": "usb",
                "serial_number": "USB-0001",
                "mac_address": "aa:bb:cc:dd:ee:ff",
                "firmware_version": "2.1.0",
                "hardware_version": "B2",
                "ip_address": "10.0.0.5",
                "location": "lobby",
                "room_id": "00000000-0000-0000-0000-000000000000",
                "meta": {"location_hint": "Entrance"},
            }
        },
    )


class SensorHeartbeat(BaseModel):
    sensor_id: Optional[UUID] = None
    serial_number: Optional[str] = None
    mac_address: Optional[str] = None
    timestamp: Optional[str] = None
    status: Optional[SensorStatusEnum] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "serial_number": "USB-0001",
                "timestamp": "2026-07-06T12:34:56.789Z",
                "status": "ONLINE",
            }
        },
    )


class SensorDisconnect(BaseModel):
    sensor_id: Optional[UUID] = None
    serial_number: Optional[str] = None
    mac_address: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "mac_address": "aa:bb:cc:dd:ee:ff",
            }
        },
    )


class SensorStatusPatch(BaseModel):
    sensor_id: Optional[UUID] = None
    serial_number: Optional[str] = None
    mac_address: Optional[str] = None
    status: SensorStatusEnum

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "serial_number": "USB-0001",
                "status": "ERROR",
            }
        },
    )
