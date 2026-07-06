from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.signalsample import SignalSample
from app.schemas.signalsample import SignalSampleCreate, SignalSampleResponse
from app.services.signalsample_service import SignalSampleService

router = APIRouter(prefix="/signals", tags=["SignalSamples"])


@router.post("/", response_model=SignalSampleResponse, status_code=status.HTTP_201_CREATED)
def create_sample(payload: SignalSampleCreate, db: Session = Depends(get_db)) -> SignalSample:
    service = SignalSampleService(db)
    sample = SignalSample(**payload.model_dump())
    return service.create(sample)


@router.get("/", response_model=List[SignalSampleResponse])
def list_samples(
    sensor_id: Optional[UUID] = None,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    service = SignalSampleService(db)
    if sensor_id:
        return service.list_for_sensor(sensor_id, start=start, end=end, limit=limit, offset=offset)
    return service.list(limit=limit, offset=offset)


@router.get("/{sample_id}", response_model=SignalSampleResponse)
def get_sample(sample_id: UUID, db: Session = Depends(get_db)):
    service = SignalSampleService(db)
    sample = service.get_by_id(sample_id)
    if not sample:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SignalSample not found")
    return sample
