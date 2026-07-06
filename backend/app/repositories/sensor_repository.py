from typing import Iterable, List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

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
