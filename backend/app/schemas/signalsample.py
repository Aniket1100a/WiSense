from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic import ConfigDict


class SignalSampleBase(BaseModel):
    sensor_id: UUID
    timestamp: str
    rssi: Optional[float] = None
    channel: Optional[int] = None
    frequency: Optional[int] = None
    noise: Optional[float] = None
    snr: Optional[float] = None
    raw_payload: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)


class SignalSampleCreate(SignalSampleBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "sensor_id": "00000000-0000-0000-0000-000000000000",
                "timestamp": "2026-07-06T12:00:00Z",
                "rssi": -65.2,
                "channel": 6,
                "frequency": 2437,
                "noise": -92.4,
                "snr": 27.8,
                "raw_payload": {"temperature": 22.3},
            }
        },
    )


class SignalSampleResponse(SignalSampleBase):
    id: UUID
    created_at: Optional[str]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "00000000-0000-0000-0000-000000000002",
                "sensor_id": "00000000-0000-0000-0000-000000000000",
                "timestamp": "2026-07-06T12:00:00Z",
                "rssi": -65.2,
                "channel": 6,
                "frequency": 2437,
                "noise": -92.4,
                "snr": 27.8,
                "raw_payload": {"temperature": 22.3},
                "created_at": "2026-07-06T12:00:00Z",
            }
        },
    )
