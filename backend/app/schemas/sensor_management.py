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

    model_config = ConfigDict(from_attributes=True)


class SensorHeartbeat(BaseModel):
    sensor_id: Optional[UUID] = None
    serial_number: Optional[str] = None
    mac_address: Optional[str] = None
    timestamp: Optional[str] = None
    status: Optional[SensorStatusEnum] = None

    model_config = ConfigDict(from_attributes=True)


class SensorDisconnect(BaseModel):
    sensor_id: Optional[UUID] = None
    serial_number: Optional[str] = None
    mac_address: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class SensorStatusPatch(BaseModel):
    sensor_id: Optional[UUID] = None
    serial_number: Optional[str] = None
    mac_address: Optional[str] = None
    status: SensorStatusEnum

    model_config = ConfigDict(from_attributes=True)
