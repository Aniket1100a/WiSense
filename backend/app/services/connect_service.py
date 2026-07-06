from app.repositories.connect_repository import ConnectRepository


class ConnectService:
    """Service layer that exposes a connectivity check to routes.

    The service composes the repository and may later orchestrate other
    components (caching, metrics, auth) while keeping controllers thin.
    """

    def __init__(self, repository: ConnectRepository) -> None:
        self.repository = repository

    def test_connection(self) -> dict[str, object]:
        """Perform a lightweight connectivity test and return a payload.

        Returns a JSON-serializable dict intended for the frontend.
        """

        ok = self.repository.ping()
        return {"ok": ok, "message": "connected" if ok else "unavailable"}
