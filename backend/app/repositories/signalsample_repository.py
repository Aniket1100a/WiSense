from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.models.signalsample import SignalSample


class SignalSampleRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, sample: SignalSample) -> SignalSample:
        self.session.add(sample)
        self.session.commit()
        self.session.refresh(sample)
        return sample

    def delete(self, sample: SignalSample) -> None:
        self.session.delete(sample)
        self.session.commit()

    def get_by_id(self, id: UUID) -> Optional[SignalSample]:
        return self.session.get(SignalSample, id)

    def get_all(self, limit: int = 100, offset: int = 0) -> List[SignalSample]:
        stmt = select(SignalSample).limit(limit).offset(offset)
        return list(self.session.scalars(stmt))

    def get_for_sensor(
        self,
        sensor_id: UUID,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[SignalSample]:
        stmt = select(SignalSample).where(SignalSample.sensor_id == sensor_id)
        if start:
            stmt = stmt.where(SignalSample.timestamp >= start)
        if end:
            stmt = stmt.where(SignalSample.timestamp <= end)
        stmt = stmt.limit(limit).offset(offset)
        return list(self.session.scalars(stmt))

    def get_latest_for_sensor(self, sensor_id: UUID) -> Optional[SignalSample]:
        stmt = (
            select(SignalSample)
            .where(SignalSample.sensor_id == sensor_id)
            .order_by(SignalSample.timestamp.desc())
            .limit(1)
        )
        return self.session.scalars(stmt).first()
