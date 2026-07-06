from typing import Generic, TypeVar

from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Base repository with a SQLAlchemy session dependency."""

    def __init__(self, session: Session) -> None:
        self.session = session
