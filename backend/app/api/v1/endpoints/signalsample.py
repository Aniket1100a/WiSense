from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.common import make_api_response, make_paginated_response
from app.database.session import get_db
from app.models.signalsample import SignalSample
from app.schemas.response import ApiResponse
from app.schemas.signalsample import SignalSampleCreate, SignalSampleResponse
from app.services.signalsample_service import SignalSampleService

router = APIRouter(prefix="/signals", tags=["SignalSamples"])


@router.post(
    "/",
    response_model=ApiResponse[SignalSampleResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a signal sample",
    description="Create a new signal sample record for a sensor.",
)
def create_sample(payload: SignalSampleCreate, db: Session = Depends(get_db)) -> dict:
    service = SignalSampleService(db)
    sample = SignalSample(**payload.model_dump())
    created_sample = service.create(sample)
    return make_api_response(data=created_sample, message="Signal sample created successfully.")


@router.get(
    "/",
    response_model=ApiResponse[List[SignalSampleResponse]],
    summary="List signal samples",
    description="Return a paginated list of signal samples, optionally filtered by sensor_id and time range.",
)
def list_samples(
    sensor_id: Optional[UUID] = Query(
        None,
        examples={"example": {"value": "00000000-0000-0000-0000-000000000000", "summary": "Filter samples by sensor UUID."}},
    ),
    start: Optional[datetime] = Query(
        None,
        examples={"example": {"value": "2026-07-06T00:00:00Z", "summary": "Start of the sample time range."}},
    ),
    end: Optional[datetime] = Query(
        None,
        examples={"example": {"value": "2026-07-06T23:59:59Z", "summary": "End of the sample time range."}},
    ),
    limit: int = Query(
        100,
        ge=1,
        examples={"default": {"value": 100, "summary": "Page size."}},
    ),
    offset: int = Query(
        0,
        ge=0,
        examples={"default": {"value": 0, "summary": "Page offset."}},
    ),
    db: Session = Depends(get_db),
) -> dict:
    service = SignalSampleService(db)
    samples = (
        service.list_for_sensor(sensor_id, start=start, end=end, limit=limit, offset=offset)
        if sensor_id
        else service.list(limit=limit, offset=offset)
    )
    return make_paginated_response(
        data=samples,
        message="Signal samples retrieved successfully.",
        limit=limit,
        offset=offset,
        count=len(samples),
    )


@router.get(
    "/{sample_id}",
    response_model=ApiResponse[SignalSampleResponse],
    summary="Get signal sample by id",
    description="Return a single signal sample by UUID.",
)
def get_sample(sample_id: UUID, db: Session = Depends(get_db)) -> dict:
    service = SignalSampleService(db)
    sample = service.get_by_id(sample_id)
    if not sample:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SignalSample not found")
    return make_api_response(data=sample, message="Signal sample retrieved successfully.")
