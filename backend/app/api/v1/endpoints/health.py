from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.endpoints.common import make_api_response
from app.database.session import get_db
from app.repositories.health_repository import HealthRepository
from app.schemas.health import HealthResponse
from app.schemas.response import ApiResponse
from app.services.health_service import HealthService

router = APIRouter(tags=["Health"])


def get_health_service(db: Session = Depends(get_db)) -> HealthService:
    """Create a health service instance for request processing."""

    repository = HealthRepository(db)
    return HealthService(repository)


@router.get(
    "/",
    response_model=ApiResponse[HealthResponse],
    summary="Service root status",
    description="Return the generic running status for the application.",
)
def read_root(service: HealthService = Depends(get_health_service)) -> dict:
    """Return the generic running status for the application."""

    status = service.get_running_status()
    return make_api_response(data=status, message="Service is running.")


@router.get(
    "/health",
    response_model=ApiResponse[HealthResponse],
    summary="Application health status",
    description="Return the application health status and service readiness.",
)
def read_health(service: HealthService = Depends(get_health_service)) -> dict:
    """Return the application health status."""

    status = service.get_health_status()
    return make_api_response(data=status, message="Health check successful.")
