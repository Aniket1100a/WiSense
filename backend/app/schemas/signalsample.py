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
    pass


class SignalSampleResponse(SignalSampleBase):
    id: UUID
    created_at: Optional[str]

    model_config = ConfigDict(from_attributes=True)
