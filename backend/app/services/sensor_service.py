from typing import Any, List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.sensor import Sensor
from app.providers.factory import ProviderFactory
from app.repositories.sensor_repository import SensorRepository
from app.repositories.signalsample_repository import SignalSampleRepository
from app.services.activity_log_service import ActivityLogService


class SensorService:
    def __init__(self, session: Session) -> None:
        self.repo = SensorRepository(session)
        self.signal_repo = SignalSampleRepository(session)
        self.activity_service = ActivityLogService(session)

    def create(self, sensor: Sensor) -> Sensor:
        return self.repo.create(sensor)

    def update(self, sensor: Sensor) -> Sensor:
        return self.repo.update(sensor)

    def delete(self, sensor: Sensor) -> None:
        return self.repo.delete(sensor)

    def get_by_id(self, id: UUID) -> Optional[Sensor]:
        return self.repo.get_by_id(id)

    def list(self, limit: int = 100, offset: int = 0) -> List[Sensor]:
        return self.repo.get_all(limit=limit, offset=offset)

    def search(self, name: Optional[str] = None, provider: Optional[str] = None) -> List[Sensor]:
        return self.repo.search(name=name, provider=provider)

    # Management operations
    def register(self, data: dict) -> Sensor:
        sensor = self.repo.register_or_update(data)
        provider_name = data.get("provider") if isinstance(data, dict) else getattr(sensor, "provider", None)
        provider = None
        if provider_name:
            provider = ProviderFactory.get(str(provider_name), sensor_info={"id": str(sensor.id)})
        try:
            setattr(sensor, "_provider", provider)
        except Exception:
            pass

        self._log_activity(
            sensor_id=sensor.id,
            action="sensor.registered",
            provider=str(provider_name) if provider_name else None,
            description="Sensor registered or updated via management API.",
            severity="INFO",
        )
        return sensor

    def heartbeat(self, *, sensor_id: Optional[str] = None, serial_number: Optional[str] = None, mac_address: Optional[str] = None, timestamp=None, status: Optional[str] = None) -> Optional[Sensor]:
        sensor = self._resolve_sensor(sensor_id, serial_number, mac_address)
        if not sensor:
            return None
        updated_sensor = self.repo.update_heartbeat(sensor, last_seen=timestamp, status=status)
        self._log_activity(
            sensor_id=updated_sensor.id,
            action="sensor.heartbeat",
            provider=str(updated_sensor.provider),
            description="Heartbeat received from sensor.",
            severity="INFO",
        )
        return updated_sensor

    def disconnect(self, *, sensor_id: Optional[str] = None, serial_number: Optional[str] = None, mac_address: Optional[str] = None) -> Optional[Sensor]:
        sensor = self._resolve_sensor(sensor_id, serial_number, mac_address)
        if not sensor:
            return None
        disconnected_sensor = self.repo.set_status(sensor, status="OFFLINE")
        self._log_activity(
            sensor_id=disconnected_sensor.id,
            action="sensor.disconnected",
            provider=str(disconnected_sensor.provider),
            description="Sensor marked as disconnected.",
            severity="WARNING",
        )
        return disconnected_sensor

    def patch_status(self, *, sensor_id: Optional[str] = None, serial_number: Optional[str] = None, mac_address: Optional[str] = None, status: str = "OFFLINE") -> Optional[Sensor]:
        sensor = self._resolve_sensor(sensor_id, serial_number, mac_address)
        if not sensor:
            return None
        patched_sensor = self.repo.set_status(sensor, status=status)
        self._log_activity(
            sensor_id=patched_sensor.id,
            action="sensor.status_updated",
            provider=str(patched_sensor.provider),
            description=f"Sensor status patched to {status}.",
            severity="INFO",
        )
        return patched_sensor

    def get_online(self, within_seconds: int = 300, limit: int = 100, offset: int = 0) -> List[Sensor]:
        return self.repo.get_online(within_seconds=within_seconds, limit=limit, offset=offset)

    def get_details(self, sensor_id: UUID, recent_activity_limit: int = 10) -> Optional[dict]:
        sensor = self.get_by_id(sensor_id)
        if not sensor:
            return None
        latest_signal = self.signal_repo.get_latest_for_sensor(sensor_id)
        recent_activity = self.activity_service.list(sensor_id=sensor_id, limit=recent_activity_limit)
        return {
            "sensor": sensor,
            "latest_signal": latest_signal,
            "recent_activity": recent_activity,
        }

    def _resolve_sensor(self, sensor_id: Optional[str], serial_number: Optional[str], mac_address: Optional[str]) -> Optional[Sensor]:
        sensor = None
        if sensor_id:
            sensor = self.get_by_id(sensor_id)
        if not sensor and serial_number:
            sensor = self.repo.get_by_serial(serial_number)
        if not sensor and mac_address:
            sensor = self.repo.get_by_mac(mac_address)
        return sensor

    def _log_activity(
        self,
        action: str,
        provider: Optional[str] = None,
        description: Optional[str] = None,
        severity: str = "INFO",
        sensor_id: Optional[UUID] = None,
    ) -> None:
        try:
            self.activity_service.log(
                action=action,
                provider=provider,
                description=description,
                severity=severity,
                sensor_id=sensor_id,
            )
        except Exception:
            pass
