from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.room import Room


class RoomRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, room: Room) -> Room:
        self.session.add(room)
        self.session.commit()
        self.session.refresh(room)
        return room

    def update(self, room: Room) -> Room:
        self.session.add(room)
        self.session.commit()
        self.session.refresh(room)
        return room

    def delete(self, room: Room) -> None:
        self.session.delete(room)
        self.session.commit()

    def get_by_id(self, id: UUID) -> Optional[Room]:
        return self.session.get(Room, id)

    def get_all(self, limit: int = 100, offset: int = 0) -> List[Room]:
        stmt = select(Room).limit(limit).offset(offset)
        return list(self.session.scalars(stmt))
