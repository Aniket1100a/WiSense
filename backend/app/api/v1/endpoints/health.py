from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.health_repository import HealthRepository
from app.schemas.health import HealthResponse
from app.services.health_service import HealthService

router = APIRouter(tags=["Health"])


def get_health_service(db: Session = Depends(get_db)) -> HealthService:
    """Create a health service instance for request processing."""

    repository = HealthRepository(db)
    return HealthService(repository)


@router.get("/", response_model=HealthResponse)
def read_root(service: HealthService = Depends(get_health_service)) -> HealthResponse:
    """Return the generic running status for the application."""

    return service.get_running_status()


@router.get("/health", response_model=HealthResponse)
def read_health(service: HealthService = Depends(get_health_service)) -> HealthResponse:
    """Return the application health status."""

    return service.get_health_status()
