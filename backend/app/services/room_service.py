from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.room import Room
from app.repositories.room_repository import RoomRepository


class RoomService:
    def __init__(self, session: Session) -> None:
        self.repo = RoomRepository(session)

    def create(self, room: Room) -> Room:
        return self.repo.create(room)

    def update(self, room: Room) -> Room:
        return self.repo.update(room)

    def delete(self, room: Room) -> None:
        return self.repo.delete(room)

    def get_by_id(self, id: UUID) -> Optional[Room]:
        return self.repo.get_by_id(id)

    def list(self, limit: int = 100, offset: int = 0) -> List[Room]:
        return self.repo.get_all(limit=limit, offset=offset)
