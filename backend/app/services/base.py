from typing import Generic, TypeVar

from app.repositories.base import BaseRepository

T = TypeVar("T")


class BaseService(Generic[T]):
    """Base service that coordinates repository access."""

    def __init__(self, repository: BaseRepository[T]) -> None:
        self.repository = repository
