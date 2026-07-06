from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.room import Room
from app.schemas.room import RoomCreate, RoomResponse, RoomUpdate
from app.services.room_service import RoomService

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(payload: RoomCreate, db: Session = Depends(get_db)) -> Room:
    service = RoomService(db)
    room = Room(**payload.model_dump())
    return service.create(room)


@router.get("/", response_model=List[RoomResponse])
def list_rooms(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    service = RoomService(db)
    return service.list(limit=limit, offset=offset)


@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: UUID, db: Session = Depends(get_db)):
    service = RoomService(db)
    room = service.get_by_id(room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return room


@router.put("/{room_id}", response_model=RoomResponse)
def update_room(room_id: UUID, payload: RoomUpdate, db: Session = Depends(get_db)):
    service = RoomService(db)
    room = service.get_by_id(room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    updates = payload.model_dump(exclude_unset=True)
    for k, v in updates.items():
        setattr(room, k, v)
    return service.update(room)


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: UUID, db: Session = Depends(get_db)):
    service = RoomService(db)
    room = service.get_by_id(room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    service.delete(room)
    return None
