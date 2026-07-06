from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.activity_log import ActivityLog


class ActivityLogRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, activity_log: ActivityLog) -> ActivityLog:
        self.session.add(activity_log)
        self.session.commit()
        self.session.refresh(activity_log)
        return activity_log

    def get_by_id(self, id: UUID) -> Optional[ActivityLog]:
        return self.session.get(ActivityLog, id)

    def list(
        self,
        sensor_id: Optional[UUID] = None,
        provider: Optional[str] = None,
        severity: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ActivityLog]:
        stmt = select(ActivityLog)
        if sensor_id:
            stmt = stmt.where(ActivityLog.sensor_id == sensor_id)
        if provider:
            stmt = stmt.where(ActivityLog.provider == provider)
        if severity:
            stmt = stmt.where(ActivityLog.severity == severity)
        stmt = stmt.order_by(ActivityLog.timestamp.desc()).limit(limit).offset(offset)
        return list(self.session.scalars(stmt))
