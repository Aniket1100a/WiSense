from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class DiscoveredSensor(BaseModel):
    provider: str
    name: str
    description: Optional[str] = None
    serial_number: Optional[str] = None
    mac_address: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    extra: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


class DiscoveryResult(BaseModel):
    provider: str
    sensors: List[DiscoveredSensor]
    timestamp: str

    model_config = ConfigDict(from_attributes=True)


class DiscoveryResponse(BaseModel):
    providers: List[str]
    sensors: List[DiscoveredSensor]
    timestamp: str

    model_config = ConfigDict(from_attributes=True)
