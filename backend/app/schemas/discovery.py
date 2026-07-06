from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class DiscoveredSensor(BaseModel):
    provider: str
    name: str
    description: Optional[str] = None
    serial_number: Optional[str] = None
    mac_address: Optional[str] = None
    room_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    extra: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "provider": "esp32",
                "name": "lab-sensor",
                "description": "Discovered sensor on the ESP32 network",
                "serial_number": "ESP32-0001",
                "mac_address": "aa:bb:cc:11:22:33",
                "room_id": "00000000-0000-0000-0000-000000000000",
                "metadata": {"location": "lab"},
                "extra": {"rssi": -60},
            }
        },
    )


class DiscoveryResult(BaseModel):
    provider: str
    sensors: List[DiscoveredSensor]
    timestamp: str

    model_config = ConfigDict(from_attributes=True)


class DiscoveryResponse(BaseModel):
    providers: List[str]
    sensors: List[DiscoveredSensor]
    timestamp: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "providers": ["esp32", "usb"],
                "sensors": [
                    {
                        "provider": "esp32",
                        "name": "lab-sensor",
                        "description": "Discovered sensor on the ESP32 network",
                        "serial_number": "ESP32-0001",
                        "mac_address": "aa:bb:cc:11:22:33",
                        "metadata": {"location": "lab"},
                        "extra": {"rssi": -60},
                    }
                ],
                "timestamp": "2026-07-06T12:00:00Z",
            }
        },
    )
