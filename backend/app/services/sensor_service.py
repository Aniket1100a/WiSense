from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.sensor import Sensor
from app.repositories.sensor_repository import SensorRepository
from app.providers.factory import ProviderFactory
from typing import Any


class SensorService:
    def __init__(self, session: Session) -> None:
        self.repo = SensorRepository(session)

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
        # initialize provider instance for runtime integration (no hardware calls)
        provider_name = None
        if isinstance(data, dict):
            provider_name = data.get("provider")
        elif hasattr(sensor, "provider"):
            provider_name = getattr(sensor, "provider")

        provider = None
        if provider_name:
            provider = ProviderFactory.get(str(provider_name), sensor_info={"id": str(sensor.id)})
        # attach provider instance for runtime use; do not persist
        try:
            setattr(sensor, "_provider", provider)
        except Exception:
            pass
        return sensor

    def heartbeat(self, *, sensor_id: Optional[str] = None, serial_number: Optional[str] = None, mac_address: Optional[str] = None, timestamp=None, status: Optional[str] = None) -> Optional[Sensor]:
        sensor = None
        if sensor_id:
            sensor = self.get_by_id(sensor_id)
        if not sensor and serial_number:
            sensor = self.repo.get_by_serial(serial_number)
        if not sensor and mac_address:
            sensor = self.repo.get_by_mac(mac_address)
        if not sensor:
            return None
        return self.repo.update_heartbeat(sensor, last_seen=timestamp, status=status)

    def disconnect(self, *, sensor_id: Optional[str] = None, serial_number: Optional[str] = None, mac_address: Optional[str] = None) -> Optional[Sensor]:
        sensor = None
        if sensor_id:
            sensor = self.get_by_id(sensor_id)
        if not sensor and serial_number:
            sensor = self.repo.get_by_serial(serial_number)
        if not sensor and mac_address:
            sensor = self.repo.get_by_mac(mac_address)
        if not sensor:
            return None
        return self.repo.set_status(sensor, status="OFFLINE")

    def patch_status(self, *, sensor_id: Optional[str] = None, serial_number: Optional[str] = None, mac_address: Optional[str] = None, status: str = "OFFLINE") -> Optional[Sensor]:
        sensor = None
        if sensor_id:
            sensor = self.get_by_id(sensor_id)
        if not sensor and serial_number:
            sensor = self.repo.get_by_serial(serial_number)
        if not sensor and mac_address:
            sensor = self.repo.get_by_mac(mac_address)
        if not sensor:
            return None
        return self.repo.set_status(sensor, status=status)

    def get_online(self, within_seconds: int = 300, limit: int = 100, offset: int = 0) -> List[Sensor]:
        return self.repo.get_online(within_seconds=within_seconds, limit=limit, offset=offset)
