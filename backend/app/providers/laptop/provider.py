from __future__ import annotations

from typing import Dict, Any, List

from app.providers.base.base_provider import BaseSensorProvider
from app.providers.registry import register_provider


@register_provider("windows_wifi")
@register_provider("linux_wifi")
class LaptopProvider(BaseSensorProvider):
    """Placeholder provider for laptop WiFi-based sensors."""

    def connect(self) -> None:
        raise NotImplementedError("Laptop provider connect not implemented in backend placeholder")

    def disconnect(self) -> None:
        raise NotImplementedError("Laptop provider disconnect not implemented in backend placeholder")

    def discover(self) -> List[Dict[str, Any]]:
        return [
            {
                "provider": "laptop",
                "name": "laptop-discovery-1",
                "description": "Mock laptop sensor",
                "serial_number": "LAP-0001",
                "mac_address": "aa:bb:cc:11:11:11",
                "metadata": {"os": "mock-os"},
            }
        ]

    def register(self) -> Dict[str, Any]:
        return {"provider": "laptop", "info": {"os": "mock", "capabilities": ["wifi","ble"]}}

    def heartbeat(self, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return {"ok": True}

    def health(self) -> Dict[str, Any]:
        return {"status": "ok", "provider": "laptop"}

    def start_capture(self) -> None:
        raise NotImplementedError()

    def stop_capture(self) -> None:
        raise NotImplementedError()

    def get_capabilities(self) -> List[Dict[str, Any]]:
        return [{"capability_name": "wifi-scan", "enabled": True}, {"capability_name": "ble-scan", "enabled": False}]

    def get_information(self) -> Dict[str, Any]:
        return {"vendor": "Generic Laptop", "model": "laptop-mock", "os": "mock-os"}

    def get_status(self) -> Dict[str, Any]:
        return {"status": "UNKNOWN"}
