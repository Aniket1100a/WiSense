from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.signalsample import SignalSample
from app.repositories.signalsample_repository import SignalSampleRepository


class SignalSampleService:
    def __init__(self, session: Session) -> None:
        self.repo = SignalSampleRepository(session)

    def create(self, sample: SignalSample) -> SignalSample:
        return self.repo.create(sample)

    def delete(self, sample: SignalSample) -> None:
        return self.repo.delete(sample)

    def get_by_id(self, id: UUID) -> Optional[SignalSample]:
        return self.repo.get_by_id(id)

    def list(self, limit: int = 100, offset: int = 0) -> List[SignalSample]:
        return self.repo.get_all(limit=limit, offset=offset)

    def list_for_sensor(
        self,
        sensor_id: UUID,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[SignalSample]:
        return self.repo.get_for_sensor(sensor_id, start=start, end=end, limit=limit, offset=offset)
