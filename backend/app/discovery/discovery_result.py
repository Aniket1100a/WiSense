from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class DiscoveredSensor:
    provider: str
    name: str
    description: Optional[str] = None
    serial_number: Optional[str] = None
    mac_address: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    extra: Optional[Dict[str, Any]] = None

    def unique_key(self) -> str:
        if self.serial_number:
            return f"{self.provider}:{self.serial_number}"
        if self.mac_address:
            return f"{self.provider}:{self.mac_address}"
        return f"{self.provider}:{self.name}"


@dataclass
class DiscoveryResult:
    providers: List[str] = field(default_factory=list)
    sensors: List[DiscoveredSensor] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "providers": self.providers,
            "sensors": [
                {
                    "provider": s.provider,
                    "name": s.name,
                    "description": s.description,
                    "serial_number": s.serial_number,
                    "mac_address": s.mac_address,
                    "metadata": s.metadata,
                    "extra": s.extra,
                }
                for s in self.sensors
            ],
            "timestamp": self.timestamp.isoformat() + "Z",
        }
