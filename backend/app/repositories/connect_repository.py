from sqlalchemy.orm import Session

from app.repositories.base import BaseRepository


class ConnectRepository(BaseRepository[None]):
    """Repository responsible for lightweight connectivity checks.

    This repository currently performs no database mutations — it exists to
    preserve the Route->Service->Repository architecture so the frontend can
    exercise a realistic code path.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def ping(self) -> bool:
        """Return True to indicate repository layer is reachable.

        In a real implementation this could perform a simple DB query.
        """

        return True
