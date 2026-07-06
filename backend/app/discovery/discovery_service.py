from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.discovery.discovery_result import DiscoveredSensor, DiscoveryResult
from app.providers.factory import ProviderFactory
from app.providers.registry import ProviderRegistry


class DiscoveryService:
    def __init__(self) -> None:
        self._latest: Optional[DiscoveryResult] = None

    def get_available_providers(self) -> List[str]:
        return list(ProviderRegistry.all_providers().keys())

    def start_discovery(self) -> DiscoveryResult:
        provider_names = self.get_available_providers()
        merged_sensors: List[DiscoveredSensor] = []
        seen = set()

        for provider_name in provider_names:
            provider = ProviderFactory.get(provider_name)
            if provider is None:
                continue

            discovered = provider.discover()
            for record in discovered:
                sensor = DiscoveredSensor(
                    provider=provider_name,
                    name=record.get("name", "unknown"),
                    description=record.get("description"),
                    serial_number=record.get("serial_number"),
                    mac_address=record.get("mac_address"),
                    metadata=record.get("metadata"),
                    extra=record.get("extra"),
                )
                key = sensor.unique_key()
                if key in seen:
                    continue
                seen.add(key)
                merged_sensors.append(sensor)

        self._latest = DiscoveryResult(
            providers=provider_names,
            sensors=merged_sensors,
            timestamp=datetime.now(timezone.utc),
        )
        return self._latest

    def get_latest(self) -> Optional[DiscoveryResult]:
        return self._latest

    def register_discovered(self, discovered_sensor: Dict[str, Optional[str]]) -> Dict[str, Optional[str]]:
        # Placeholder: real registration is handled in the discovery endpoint via SensorService.
        return discovered_sensor
