from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.sensor import Sensor
from app.repositories.sensor_repository import SensorRepository


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
