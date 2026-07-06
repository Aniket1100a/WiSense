from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.common import make_api_response
from app.database.session import get_db
from app.discovery.discovery_service import DiscoveryService
from app.schemas.discovery import DiscoveryResponse, DiscoveredSensor
from app.schemas.response import ApiResponse
from app.schemas.sensor import SensorResponse
from app.services.sensor_service import SensorService

router = APIRouter(prefix="/discovery", tags=["Discovery"])

_discovery_service = DiscoveryService()


@router.get(
    "/providers",
    response_model=ApiResponse[List[str]],
    status_code=status.HTTP_200_OK,
    summary="List discovery providers",
    description="Return the names of all registered provider implementations available for discovery.",
)
def list_discovery_providers() -> dict:
    providers = _discovery_service.get_available_providers()
    return make_api_response(data=providers, message="Discovery providers retrieved successfully.")


@router.post(
    "/start",
    response_model=ApiResponse[DiscoveryResponse],
    status_code=status.HTTP_200_OK,
    summary="Start discovery",
    description="Run discovery across all registered providers and merge results.",
)
def start_discovery() -> dict:
    result = _discovery_service.start_discovery()
    payload = DiscoveryResponse(
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
    return make_api_response(data=payload, message="Discovery completed successfully.")


@router.get(
    "/results",
    response_model=ApiResponse[DiscoveryResponse],
    status_code=status.HTTP_200_OK,
    summary="Get latest discovery results",
    description="Return the most recent discovery results produced by a prior discovery call.",
)
def get_discovery_results() -> dict:
    result = _discovery_service.get_latest()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No discovery results available")
    payload = DiscoveryResponse(
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
    return make_api_response(data=payload, message="Latest discovery results returned successfully.")


@router.post(
    "/register",
    response_model=ApiResponse[SensorResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Register discovered sensor",
    description="Register a discovered sensor into the Sensor Platform.",
)
def register_discovered_sensor(payload: DiscoveredSensor, db: Session = Depends(get_db)) -> dict:
    sensor_service = SensorService(db)
    register_data: Dict[str, object] = payload.model_dump()
    sensor = sensor_service.register(register_data)
    if not sensor:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to register discovered sensor")
    return make_api_response(data=sensor, message="Discovered sensor registered successfully.")
