from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.endpoints.common import make_api_response
from app.database.session import get_db
from app.repositories.connect_repository import ConnectRepository
from app.schemas.connect import ConnectResponse
from app.schemas.response import ApiResponse
from app.services.connect_service import ConnectService

router = APIRouter()


def get_connect_service(db: Session = Depends(get_db)) -> ConnectService:
    """Dependency factory for `ConnectService` using a request-scoped session."""

    repository = ConnectRepository(db)
    return ConnectService(repository)


@router.get(
    "/connect",
    response_model=ApiResponse[ConnectResponse],
    tags=["Connect"],
    summary="Verify backend connectivity",
    description="Return a simple connectivity payload used by the frontend to validate API reachability.",
)
def connect(service: ConnectService = Depends(get_connect_service)) -> dict:
    """Endpoint used by the frontend to verify backend connectivity for testing."""

    payload = service.test_connection()
    return make_api_response(data=payload, message="Connection verified.")
