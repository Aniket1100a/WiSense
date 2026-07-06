from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.activity_log import ActivityLog
from app.repositories.activity_log_repository import ActivityLogRepository


class ActivityLogService:
    def __init__(self, session: Session) -> None:
        self.repo = ActivityLogRepository(session)

    def log(
        self,
        action: str,
        provider: Optional[str] = None,
        description: Optional[str] = None,
        severity: str = "INFO",
        sensor_id: Optional[UUID] = None,
    ) -> ActivityLog:
        activity = ActivityLog(
            action=action,
            provider=provider,
            description=description,
            severity=severity,
            sensor_id=sensor_id,
        )
        return self.repo.create(activity)

    def list(
        self,
        sensor_id: Optional[UUID] = None,
        provider: Optional[str] = None,
        severity: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ActivityLog]:
        return self.repo.list(
            sensor_id=sensor_id,
            provider=provider,
            severity=severity,
            limit=limit,
            offset=offset,
        )
