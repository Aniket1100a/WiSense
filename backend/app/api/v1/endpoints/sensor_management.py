from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.common import make_api_response, make_paginated_response
from app.database.session import get_db
from app.schemas.response import ApiResponse
from app.schemas.sensor import SensorResponse
from app.schemas.sensor_management import (
    SensorDisconnect,
    SensorHeartbeat,
    SensorRegister,
    SensorStatusPatch,
)
from app.services.sensor_service import SensorService

router = APIRouter(prefix="/sensors", tags=["Sensors Management"])


@router.post(
    "/register",
    response_model=ApiResponse[SensorResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Register or update a sensor",
    description="Register a new sensor or update an existing sensor based on serial number or MAC address.",
)
def register_sensor(payload: SensorRegister, db: Session = Depends(get_db)) -> dict:
    """Register a sensor. If a sensor with the same `serial_number` or `mac_address` exists, update it."""
    svc = SensorService(db)
    data = payload.model_dump()
    sensor = svc.register(data)
    return make_api_response(data=sensor, message="Sensor registered successfully.")


@router.post(
    "/heartbeat",
    response_model=ApiResponse[SensorResponse],
    status_code=status.HTTP_200_OK,
    summary="Sensor heartbeat",
    description="Receive heartbeat messages from sensors. Updates last_seen and status.",
)
def sensor_heartbeat(payload: SensorHeartbeat, db: Session = Depends(get_db)) -> dict:
    svc = SensorService(db)
    ts = None
    if payload.timestamp:
        try:
            ts = datetime.fromisoformat(payload.timestamp)
        except Exception:
            ts = None
    sensor = svc.heartbeat(
        sensor_id=str(payload.sensor_id) if payload.sensor_id else None,
        serial_number=payload.serial_number,
        mac_address=payload.mac_address,
        timestamp=ts,
        status=payload.status.value if payload.status else None,
    )
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    return make_api_response(data=sensor, message="Heartbeat recorded successfully.")


@router.post(
    "/disconnect",
    response_model=ApiResponse[SensorResponse],
    status_code=status.HTTP_200_OK,
    summary="Sensor disconnect",
    description="Mark a sensor as disconnected / offline.",
)
def sensor_disconnect(payload: SensorDisconnect, db: Session = Depends(get_db)) -> dict:
    svc = SensorService(db)
    sensor = svc.disconnect(
        sensor_id=str(payload.sensor_id) if payload.sensor_id else None,
        serial_number=payload.serial_number,
        mac_address=payload.mac_address,
    )
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    return make_api_response(data=sensor, message="Sensor disconnected successfully.")


@router.get(
    "/online",
    response_model=ApiResponse[List[SensorResponse]],
    status_code=status.HTTP_200_OK,
    summary="List online sensors",
    description="Return sensors that are currently online or that have reported recently.",
)
def get_online_sensors(
    within_seconds: int = Query(
        300,
        ge=1,
        examples={"default": {"value": 300, "summary": "Within how many seconds sensor should still be considered online."}},
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
    svc = SensorService(db)
    sensors = svc.get_online(within_seconds=within_seconds, limit=limit, offset=offset)
    return make_paginated_response(
        data=sensors,
        message="Online sensors retrieved successfully.",
        limit=limit,
        offset=offset,
        count=len(sensors),
    )


@router.patch(
    "/status",
    response_model=ApiResponse[SensorResponse],
    status_code=status.HTTP_200_OK,
    summary="Patch sensor status",
    description="Patch a sensor's status based on its identifiers.",
)
def patch_sensor_status(payload: SensorStatusPatch, db: Session = Depends(get_db)) -> dict:
    svc = SensorService(db)
    sensor = svc.patch_status(
        sensor_id=str(payload.sensor_id) if payload.sensor_id else None,
        serial_number=payload.serial_number,
        mac_address=payload.mac_address,
        status=payload.status.value,
    )
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    return make_api_response(data=sensor, message="Sensor status updated successfully.")
