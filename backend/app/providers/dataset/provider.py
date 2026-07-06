from __future__ import annotations

from typing import Dict, Any, List

from app.providers.base.base_provider import BaseSensorProvider
from app.providers.registry import register_provider


@register_provider("dataset")
class DatasetProvider(BaseSensorProvider):
    """Placeholder provider for replay/dataset sensors."""

    def connect(self) -> None:
        # Datasets are local; no connection required
        return None

    def disconnect(self) -> None:
        return None

    def discover(self) -> List[Dict[str, Any]]:
        return [
            {
                "provider": "dataset",
                "name": "dataset-discovery-1",
                "description": "Mock replay dataset sensor",
                "serial_number": "DATA-0001",
                "mac_address": "aa:bb:cc:33:33:33",
                "metadata": {"type": "dataset"},
            }
        ]

    def register(self) -> Dict[str, Any]:
        return {"provider": "dataset", "info": {"type": "replay"}}

    def heartbeat(self, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return {"ok": True}

    def health(self) -> Dict[str, Any]:
        return {"status": "ok", "provider": "dataset"}

    def start_capture(self) -> None:
        raise NotImplementedError()

    def stop_capture(self) -> None:
        raise NotImplementedError()

    def get_capabilities(self) -> List[Dict[str, Any]]:
        return [{"capability_name": "replay", "enabled": True}]

    def get_information(self) -> Dict[str, Any]:
        return {"type": "replay-dataset", "source": "local"}

    def get_status(self) -> Dict[str, Any]:
        return {"status": "STANDBY"}
