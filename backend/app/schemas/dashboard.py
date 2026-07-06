from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DashboardOverview(BaseModel):
    active_devices: int
    offline_devices: int
    warning_devices: int
    error_devices: int
    active_rooms: int
    providers: List[Dict[str, Any]]
    avg_signal: Optional[float] = None
    latest_discovery: Optional[Dict[str, Any]] = None
    last_update: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "active_devices": 12,
                "offline_devices": 3,
                "warning_devices": 1,
                "error_devices": 0,
                "active_rooms": 4,
                "providers": [
                    {"provider": "esp32", "count": 8},
                    {"provider": "usb_adapter", "count": 4},
                ],
                "avg_signal": -45.7,
                "latest_discovery": {
                    "provider_count": 5,
                    "sensor_count": 12,
                    "timestamp": "2026-07-06T12:00:00Z",
                },
                "last_update": "2026-07-06T12:00:00Z",
            }
        },
    )


class ChartData(BaseModel):
    labels: List[str]
    values: List[int]

    model_config = ConfigDict(from_attributes=True)


class SignalHistoryData(BaseModel):
    labels: List[str]
    avg_rssi: List[Optional[float]]
    counts: List[int]

    model_config = ConfigDict(from_attributes=True)
