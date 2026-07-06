from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.sensor import SensorResponse
from app.schemas.sensor_management import (
    SensorRegister,
    SensorHeartbeat,
    SensorDisconnect,
    SensorStatusPatch,
)
from app.services.sensor_service import SensorService

router = APIRouter(prefix="/sensors", tags=["Sensors Management"])


@router.post(
    "/register",
    response_model=SensorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register or update a sensor",
    description="Register a new sensor or update an existing sensor if the same serial number or MAC address exists.",
)
def register_sensor(payload: SensorRegister, db: Session = Depends(get_db)):
    """Register a sensor. If a sensor with the same `serial_number` or `mac_address` exists, update it."""
    svc = SensorService(db)
    data = payload.model_dump()
    sensor = svc.register(data)
    return sensor


@router.post(
    "/heartbeat",
    response_model=SensorResponse,
    status_code=status.HTTP_200_OK,
    summary="Sensor heartbeat",
    description="Receive heartbeat messages from sensors. Accepts `sensor_id`, `serial_number`, or `mac_address` to identify the sensor. Updates `last_seen` and sets status to ONLINE by default.",
)
def sensor_heartbeat(payload: SensorHeartbeat, db: Session = Depends(get_db)):
    svc = SensorService(db)
    # parse timestamp if provided
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
    return sensor


@router.post(
    "/disconnect",
    response_model=SensorResponse,
    status_code=status.HTTP_200_OK,
    summary="Sensor disconnect",
    description="Mark a sensor as disconnected/offline. Accepts `sensor_id`, `serial_number`, or `mac_address` to identify the sensor.",
)
def sensor_disconnect(payload: SensorDisconnect, db: Session = Depends(get_db)):
    svc = SensorService(db)
    sensor = svc.disconnect(
        sensor_id=str(payload.sensor_id) if payload.sensor_id else None,
        serial_number=payload.serial_number,
        mac_address=payload.mac_address,
    )
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    return sensor


@router.get(
    "/online",
    response_model=List[SensorResponse],
    status_code=status.HTTP_200_OK,
    summary="List online sensors",
    description="Return sensors that are currently online or which have reported within the supplied `within_seconds` window (default 300s).",
)
def get_online_sensors(within_seconds: int = 300, limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    svc = SensorService(db)
    return svc.get_online(within_seconds=within_seconds, limit=limit, offset=offset)


@router.patch(
    "/status",
    response_model=SensorResponse,
    status_code=status.HTTP_200_OK,
    summary="Patch sensor status",
    description="Patch a sensor's status (e.g., set to OFFLINE, ERROR, ONLINE). Identify the sensor by `sensor_id`, `serial_number`, or `mac_address`.",
)
def patch_sensor_status(payload: SensorStatusPatch, db: Session = Depends(get_db)):
    svc = SensorService(db)
    sensor = svc.patch_status(
        sensor_id=str(payload.sensor_id) if payload.sensor_id else None,
        serial_number=payload.serial_number,
        mac_address=payload.mac_address,
        status=payload.status.value,
    )
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    return sensor
