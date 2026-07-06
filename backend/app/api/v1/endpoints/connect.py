from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.connect_repository import ConnectRepository
from app.schemas.connect import ConnectResponse
from app.services.connect_service import ConnectService

router = APIRouter()


def get_connect_service(db: Session = Depends(get_db)) -> ConnectService:
    """Dependency factory for `ConnectService` using a request-scoped session."""

    repository = ConnectRepository(db)
    return ConnectService(repository)


@router.get("/connect", response_model=ConnectResponse, tags=["Connect"])
def connect(service: ConnectService = Depends(get_connect_service)) -> ConnectResponse:
    """Endpoint used by the frontend to verify backend connectivity for testing.

    This endpoint intentionally keeps logic minimal and returns a stable
    JSON payload that frontend code can use to confirm an API connection.
    """

    return service.test_connection()
