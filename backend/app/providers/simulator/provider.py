from __future__ import annotations

from typing import Dict, Any, List

from app.providers.base.base_provider import BaseSensorProvider
from app.providers.registry import register_provider


@register_provider("simulator")
class SimulatorProvider(BaseSensorProvider):
    """Placeholder provider for simulated sensors."""

    def connect(self) -> None:
        return None

    def disconnect(self) -> None:
        return None

    def discover(self) -> List[Dict[str, Any]]:
        return []

    def register(self) -> Dict[str, Any]:
        return {"provider": "simulator", "info": {"mode": "mock"}}

    def heartbeat(self, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return {"ok": True}

    def health(self) -> Dict[str, Any]:
        return {"status": "ok", "provider": "simulator"}

    def start_capture(self) -> None:
        return None

    def stop_capture(self) -> None:
        return None

    def get_capabilities(self) -> List[Dict[str, Any]]:
        return [{"capability_name": "simulated-sensor", "enabled": True}]

    def get_information(self) -> Dict[str, Any]:
        return {"vendor": "sim", "model": "sim-mock"}

    def get_status(self) -> Dict[str, Any]:
        return {"status": "SIMULATED"}
