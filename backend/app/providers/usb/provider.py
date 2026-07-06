from __future__ import annotations

from typing import Dict, Any, List

from app.providers.base.base_provider import BaseSensorProvider
from app.providers.registry import register_provider


@register_provider("usb_adapter")
class USBAdapterProvider(BaseSensorProvider):
    """Placeholder provider for USB WiFi adapters or similar devices."""

    def connect(self) -> None:
        raise NotImplementedError()

    def disconnect(self) -> None:
        raise NotImplementedError()

    def discover(self) -> List[Dict[str, Any]]:
        return []

    def register(self) -> Dict[str, Any]:
        return {"provider": "usb_adapter", "info": {"capabilities": ["usb-wifi"]}}

    def heartbeat(self, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return {"ok": True}

    def health(self) -> Dict[str, Any]:
        return {"status": "ok", "provider": "usb_adapter"}

    def start_capture(self) -> None:
        raise NotImplementedError()

    def stop_capture(self) -> None:
        raise NotImplementedError()

    def get_capabilities(self) -> List[Dict[str, Any]]:
        return [{"capability_name": "usb-wifi", "enabled": True}]

    def get_information(self) -> Dict[str, Any]:
        return {"vendor": "USB Vendor", "model": "usb-mock"}

    def get_status(self) -> Dict[str, Any]:
        return {"status": "UNKNOWN"}
