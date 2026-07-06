from app.core.constants import HEALTH_STATUS_HEALTHY, HEALTH_STATUS_RUNNING
from app.repositories.health_repository import HealthRepository
from app.services.base import BaseService


class HealthService(BaseService[None]):
    """Service layer for health endpoint orchestration."""

    def __init__(self, repository: HealthRepository) -> None:
        super().__init__(repository)

    def get_running_status(self) -> dict[str, str]:
        """Return the application running status."""

        return {"status": HEALTH_STATUS_RUNNING}

    def get_health_status(self) -> dict[str, str]:
        """Return the API health status."""

        return {"status": HEALTH_STATUS_HEALTHY}
