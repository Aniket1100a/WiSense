from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.discovery.discovery_service import DiscoveryService
from app.schemas.discovery import DiscoveryResponse, DiscoveredSensor
from app.schemas.sensor import SensorResponse
from app.services.sensor_service import SensorService

router = APIRouter(prefix="/discovery", tags=["Discovery"])

_discovery_service = DiscoveryService()


@router.get(
    "/providers",
    response_model=List[str],
    status_code=status.HTTP_200_OK,
    summary="List available discovery providers",
    description="Return the names of all registered provider implementations available for discovery.",
)
def list_discovery_providers() -> List[str]:
    return _discovery_service.get_available_providers()


@router.post(
    "/start",
    response_model=DiscoveryResponse,
    status_code=status.HTTP_200_OK,
    summary="Start discovery across all providers",
    description="Run discovery on every registered provider and merge the resulting discovered sensors.",
)
def start_discovery() -> DiscoveryResponse:
    result = _discovery_service.start_discovery()
    return DiscoveryResponse(
        providers=result.providers,
        sensors=[
            DiscoveredSensor(
                provider=s.provider,
                name=s.name,
                description=s.description,
                serial_number=s.serial_number,
                mac_address=s.mac_address,
                metadata=s.metadata,
                extra=s.extra,
            )
            for s in result.sensors
        ],
        timestamp=result.timestamp.isoformat(),
    )


@router.get(
    "/results",
    response_model=DiscoveryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get latest discovery results",
    description="Return the most recent discovery response produced by a prior `POST /api/v1/discovery/start` call.",
)
def get_discovery_results() -> DiscoveryResponse:
    result = _discovery_service.get_latest()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No discovery results available")
    return DiscoveryResponse(
        providers=result.providers,
        sensors=[
            DiscoveredSensor(
                provider=s.provider,
                name=s.name,
                description=s.description,
                serial_number=s.serial_number,
                mac_address=s.mac_address,
                metadata=s.metadata,
                extra=s.extra,
            )
            for s in result.sensors
        ],
        timestamp=result.timestamp.isoformat(),
    )


@router.post(
    "/register",
    response_model=SensorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a discovered sensor",
    description="Take a discovered sensor from discovery results and register it into the Sensor Platform.",
)
def register_discovered_sensor(payload: DiscoveredSensor, db: Session = Depends(get_db)) -> SensorResponse:
    sensor_service = SensorService(db)
    register_data: Dict[str, object] = payload.model_dump()
    sensor = sensor_service.register(register_data)
    if not sensor:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to register discovered sensor")
    return sensor
