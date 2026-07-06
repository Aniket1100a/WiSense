from __future__ import annotations

from typing import Dict, Any, List

from app.providers.base.base_provider import BaseSensorProvider
from app.providers.registry import register_provider


@register_provider("esp32")
class ESP32Provider(BaseSensorProvider):
    """Placeholder provider for ESP32 devices."""

    def connect(self) -> None:
        raise NotImplementedError("ESP32 hardware connect not implemented in backend placeholder")

    def disconnect(self) -> None:
        raise NotImplementedError("ESP32 hardware disconnect not implemented in backend placeholder")

    def discover(self) -> List[Dict[str, Any]]:
        raise NotImplementedError("ESP32 discovery not implemented")

    def register(self) -> Dict[str, Any]:
        # Return mocked registration information
        return {"provider": "esp32", "info": {"model": "esp32-mock", "capabilities": ["wifi"]}}

    def heartbeat(self, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return {"ok": True, "received": bool(payload)}

    def health(self) -> Dict[str, Any]:
        return {"status": "ok", "provider": "esp32"}

    def start_capture(self) -> None:
        raise NotImplementedError("start_capture not implemented for esp32 placeholder")

    def stop_capture(self) -> None:
        raise NotImplementedError("stop_capture not implemented for esp32 placeholder")

    def get_capabilities(self) -> List[Dict[str, Any]]:
        return [{"capability_name": "wifi-scan", "enabled": True}]

    def get_information(self) -> Dict[str, Any]:
        return {"vendor": "Espressif", "model": "ESP32-MOCK", "firmware": "0.0.1"}

    def get_status(self) -> Dict[str, Any]:
        return {"status": "UNKNOWN", "uptime": 0}
