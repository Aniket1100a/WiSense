from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.common import make_api_response
from app.database.session import get_db
from app.schemas.activity_log import ActivityLogResponse
from app.schemas.response import ApiResponse
from app.services.activity_log_service import ActivityLogService

router = APIRouter(prefix="/activity", tags=["Activity"])


def get_activity_log_service(db: Session = Depends(get_db)) -> ActivityLogService:
    return ActivityLogService(db)


@router.get(
    "/activity",
    response_model=ApiResponse[list[ActivityLogResponse]],
    status_code=status.HTTP_200_OK,
    summary="List activity log entries",
    description="Return activity log entries for sensors and provider operations.",
)
def list_activity_logs(
    sensor_id: Optional[UUID] = Query(None, description="Filter activity by sensor UUID."),
    provider: Optional[str] = Query(None, description="Filter activity by provider."),
    severity: Optional[str] = Query(None, description="Filter activity by severity level."),
    limit: int = Query(100, ge=1, le=500, description="Max records returned."),
    offset: int = Query(0, ge=0, description="Pagination offset."),
    service: ActivityLogService = Depends(get_activity_log_service),
) -> dict:
    entries = service.list(
        sensor_id=sensor_id,
        provider=provider,
        severity=severity,
        limit=limit,
        offset=offset,
    )
    return make_api_response(
        data=entries,
        message="Activity log entries retrieved successfully.",
    )
