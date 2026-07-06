from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.common import make_api_response, make_paginated_response
from app.database.session import get_db
from app.models.sensor import Sensor
from app.schemas.response import ApiResponse
from app.schemas.sensor import SensorCreate, SensorResponse, SensorUpdate
from app.services.sensor_service import SensorService

router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.post(
    "/",
    response_model=ApiResponse[SensorResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a sensor",
    description="Create a new sensor record in the Sensor Platform.",
)
def create_sensor(payload: SensorCreate, db: Session = Depends(get_db)) -> dict:
    service = SensorService(db)
    sensor = Sensor(**payload.model_dump())
    created_sensor = service.create(sensor)
    return make_api_response(
        data=created_sensor,
        message="Sensor created successfully.",
    )


@router.get(
    "/",
    response_model=ApiResponse[List[SensorResponse]],
    summary="List sensors",
    description="Return a paginated list of sensors. Use `limit` and `offset` to page results.",
)
def list_sensors(
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
    service = SensorService(db)
    sensors = service.list(limit=limit, offset=offset)
    return make_paginated_response(
        data=sensors,
        message="Sensors retrieved successfully.",
        limit=limit,
        offset=offset,
        count=len(sensors),
    )


@router.get(
    "/search",
    response_model=ApiResponse[List[SensorResponse]],
    summary="Search sensors",
    description="Search sensors by name and / or provider.",
)
def search_sensors(
    name: str | None = Query(
        None,
        examples={"example": {"value": "lobby", "summary": "Search by sensor name."}},
    ),
    provider: str | None = Query(
        None,
        examples={"example": {"value": "esp32", "summary": "Search by provider."}},
    ),
    db: Session = Depends(get_db),
) -> dict:
    service = SensorService(db)
    sensors = service.search(name=name, provider=provider)
    return make_api_response(
        data=sensors,
        message="Search completed successfully.",
    )


@router.get(
    "/{sensor_id}",
    response_model=ApiResponse[SensorResponse],
    summary="Get sensor by id",
    description="Return a single sensor by its UUID.",
)
def get_sensor(sensor_id: UUID, db: Session = Depends(get_db)) -> dict:
    service = SensorService(db)
    sensor = service.get_by_id(sensor_id)
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    return make_api_response(data=sensor, message="Sensor retrieved successfully.")


@router.put(
    "/{sensor_id}",
    response_model=ApiResponse[SensorResponse],
    summary="Update sensor",
    description="Update an existing sensor record by UUID.",
)
def update_sensor(sensor_id: UUID, payload: SensorUpdate, db: Session = Depends(get_db)) -> dict:
    service = SensorService(db)
    sensor = service.get_by_id(sensor_id)
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    updates = payload.model_dump(exclude_unset=True)
    for k, v in updates.items():
        setattr(sensor, k, v)
    updated_sensor = service.update(sensor)
    return make_api_response(data=updated_sensor, message="Sensor updated successfully.")


@router.delete(
    "/{sensor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete sensor",
    description="Delete a sensor by UUID. Returns 204 No Content on success.",
)
def delete_sensor(sensor_id: UUID, db: Session = Depends(get_db)):
    service = SensorService(db)
    sensor = service.get_by_id(sensor_id)
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    service.delete(sensor)
    return None
