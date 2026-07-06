from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.discovery.discovery_service import DiscoveryService
from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:
    def __init__(self, session: Session) -> None:
        self.repo = DashboardRepository(session)
        self.discovery_service = DiscoveryService()

    def get_overview(self) -> Dict[str, Any]:
        status_counts = self.repo.get_device_status_counts()
        provider_counts = self.repo.get_provider_counts()

        overview = {
            "active_devices": status_counts.get("ONLINE", 0),
            "offline_devices": status_counts.get("OFFLINE", 0),
            "warning_devices": status_counts.get("CONNECTING", 0),
            "error_devices": status_counts.get("ERROR", 0),
            "active_rooms": self.repo.get_active_rooms_count(),
            "providers": provider_counts,
            "avg_signal": self.repo.get_avg_signal_rssi(),
            "latest_discovery": self._get_latest_discovery_summary(),
            "last_update": datetime.now(timezone.utc).isoformat(),
        }
        return overview

    def _get_latest_discovery_summary(self) -> Optional[Dict[str, Any]]:
        latest = self.discovery_service.get_latest()
        if not latest:
            return None
        return {
            "provider_count": len(latest.providers),
            "sensor_count": len(latest.sensors),
            "timestamp": latest.timestamp.isoformat(),
        }

    def get_device_health_chart(self) -> Dict[str, Any]:
        counts = self.repo.get_sensor_health_counts()
        labels = ["ONLINE", "OFFLINE", "CONNECTING", "ERROR", "DISABLED"]
        return {
            "labels": labels,
            "values": [counts.get(label, 0) for label in labels],
        }

    def get_signal_history_chart(self) -> Dict[str, Any]:
        history = self.repo.get_signal_history()
        labels = [entry["day"] or "" for entry in history]
        return {
            "labels": labels,
            "avg_rssi": [entry["avg_rssi"] for entry in history],
            "counts": [entry["count"] for entry in history],
        }

    def get_provider_distribution(self) -> Dict[str, Any]:
        provider_counts = self.repo.get_provider_counts()
        return {
            "labels": [entry["provider"] for entry in provider_counts],
            "values": [entry["count"] for entry in provider_counts],
        }

    def get_status_distribution(self) -> Dict[str, Any]:
        counts = self.repo.get_sensor_health_counts()
        labels = ["ONLINE", "OFFLINE", "CONNECTING", "ERROR", "DISABLED"]
        return {
            "labels": labels,
            "values": [counts.get(label, 0) for label in labels],
        }
