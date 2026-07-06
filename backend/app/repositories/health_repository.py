from sqlalchemy.orm import Session

from app.repositories.base import BaseRepository


class HealthRepository(BaseRepository[None]):
    """Repository placeholder for health check persistence operations."""

    def __init__(self, session: Session) -> None:
        super().__init__(session)
