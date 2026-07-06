from typing import Iterable, List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from sqlalchemy import and_

from app.models.sensor import Sensor


class SensorRepository:
    """Repository for Sensor DB operations. No business logic here."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, sensor: Sensor) -> Sensor:
        self.session.add(sensor)
        self.session.commit()
        self.session.refresh(sensor)
        return sensor

    def update(self, sensor: Sensor) -> Sensor:
        self.session.add(sensor)
        self.session.commit()
        self.session.refresh(sensor)
        return sensor

    def delete(self, sensor: Sensor) -> None:
        self.session.delete(sensor)
        self.session.commit()

    def get_by_id(self, id: UUID) -> Optional[Sensor]:
        return self.session.get(Sensor, id)

    def get_all(self, limit: int = 100, offset: int = 0) -> List[Sensor]:
        stmt = select(Sensor).limit(limit).offset(offset)
        return list(self.session.scalars(stmt))

    def search(self, name: Optional[str] = None, provider: Optional[str] = None) -> List[Sensor]:
        stmt = select(Sensor)
        if name:
            stmt = stmt.where(Sensor.name.ilike(f"%{name}%"))
        if provider:
            stmt = stmt.where(Sensor.provider == provider)
        return list(self.session.scalars(stmt))

    def get_by_serial(self, serial_number: str) -> Optional[Sensor]:
        if not serial_number:
            return None
        stmt = select(Sensor).where(Sensor.serial_number == serial_number)
        return self.session.scalars(stmt).first()

    def get_by_mac(self, mac_address: str) -> Optional[Sensor]:
        if not mac_address:
            return None
        stmt = select(Sensor).where(Sensor.mac_address == mac_address)
        return self.session.scalars(stmt).first()

    def register_or_update(self, data: dict) -> Sensor:
        """Register a sensor or update an existing one based on serial or mac match."""
        # normalize incoming payload keys: `metadata` -> `meta`
        if "metadata" in data and "meta" not in data:
            data["meta"] = data.pop("metadata")
        sensor = None
        # Prefer explicit id if provided
        sid = data.get("id")
        if sid:
            sensor = self.get_by_id(sid)

        if not sensor:
            sensor = None
            if data.get("serial_number"):
                sensor = self.get_by_serial(data.get("serial_number"))
        if not sensor and data.get("mac_address"):
            sensor = self.get_by_mac(data.get("mac_address"))

        if sensor:
            # apply provided fields
            for k, v in data.items():
                if hasattr(sensor, k) and v is not None:
                    setattr(sensor, k, v)
            self.session.add(sensor)
            self.session.commit()
            self.session.refresh(sensor)
            return sensor

        # create new sensor
        new_sensor = Sensor(**data)
        self.session.add(new_sensor)
        self.session.commit()
        self.session.refresh(new_sensor)
        return new_sensor

    def update_heartbeat(self, sensor: Sensor, last_seen: Optional[datetime] = None, status: Optional[str] = None) -> Sensor:
        now = datetime.now(timezone.utc)
        sensor.last_seen = last_seen or now
        if status:
            sensor.status = status
        else:
            # default to online on heartbeat
            try:
                sensor.status = type(sensor).status.type.python_type("ONLINE")
            except Exception:
                sensor.status = sensor.status
        self.session.add(sensor)
        self.session.commit()
        self.session.refresh(sensor)
        return sensor

    def set_status(self, sensor: Sensor, status: str) -> Sensor:
        sensor.status = status
        sensor.last_seen = datetime.now(timezone.utc)
        self.session.add(sensor)
        self.session.commit()
        self.session.refresh(sensor)
        return sensor

    def get_online(self, within_seconds: int = 300, limit: int = 100, offset: int = 0) -> List[Sensor]:
        """Return sensors considered online. If `within_seconds` is provided, sensors with recent last_seen are included."""
        cutoff = datetime.now(timezone.utc) - timedelta(seconds=within_seconds)
        stmt = select(Sensor).where(
            (Sensor.status == "ONLINE") | (Sensor.last_seen != None and Sensor.last_seen >= cutoff)
        ).limit(limit).offset(offset)
        return list(self.session.scalars(stmt))
