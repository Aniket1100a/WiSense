from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.sensor import Sensor
from app.schemas.sensor import SensorCreate, SensorResponse, SensorUpdate
from app.services.sensor_service import SensorService

router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.post("/", response_model=SensorResponse, status_code=status.HTTP_201_CREATED)
def create_sensor(
    payload: SensorCreate, db: Session = Depends(get_db)
) -> Sensor:
    service = SensorService(db)
    sensor = Sensor(**payload.model_dump())
    return service.create(sensor)


@router.get("/", response_model=List[SensorResponse])
def list_sensors(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    service = SensorService(db)
    return service.list(limit=limit, offset=offset)


@router.get("/search", response_model=List[SensorResponse])
def search_sensors(name: str | None = None, provider: str | None = None, db: Session = Depends(get_db)):
    service = SensorService(db)
    return service.search(name=name, provider=provider)


@router.get("/{sensor_id}", response_model=SensorResponse)
def get_sensor(sensor_id: UUID, db: Session = Depends(get_db)):
    service = SensorService(db)
    sensor = service.get_by_id(sensor_id)
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    return sensor


@router.put("/{sensor_id}", response_model=SensorResponse)
def update_sensor(sensor_id: UUID, payload: SensorUpdate, db: Session = Depends(get_db)):
    service = SensorService(db)
    sensor = service.get_by_id(sensor_id)
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    updates = payload.model_dump(exclude_unset=True)
    for k, v in updates.items():
        setattr(sensor, k, v)
    return service.update(sensor)


@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor(sensor_id: UUID, db: Session = Depends(get_db)):
    service = SensorService(db)
    sensor = service.get_by_id(sensor_id)
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    service.delete(sensor)
    return None
