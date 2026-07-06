from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.common import make_api_response, make_paginated_response
from app.database.session import get_db
from app.models.room import Room
from app.schemas.response import ApiResponse
from app.schemas.room import RoomCreate, RoomResponse, RoomUpdate
from app.services.room_service import RoomService

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.post(
    "/",
    response_model=ApiResponse[RoomResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a room",
    description="Create a new room record in the Sensor Platform.",
)
def create_room(payload: RoomCreate, db: Session = Depends(get_db)) -> dict:
    service = RoomService(db)
    room = Room(**payload.model_dump())
    created_room = service.create(room)
    return make_api_response(data=created_room, message="Room created successfully.")


@router.get(
    "/",
    response_model=ApiResponse[List[RoomResponse]],
    summary="List rooms",
    description="Return a paginated list of rooms.",
)
def list_rooms(
    limit: int = Query(
        100,
        ge=1,
        examples={"default": {"value": 100, "summary": "Page size."}},
    ),
    offset: int = Query(
        0,
        ge=0,
        examples={"default": {"value": 0, "summary": "Page offset."}},
    ),
    db: Session = Depends(get_db),
) -> dict:
    service = RoomService(db)
    rooms = service.list(limit=limit, offset=offset)
    return make_paginated_response(
        data=rooms,
        message="Rooms retrieved successfully.",
        limit=limit,
        offset=offset,
        count=len(rooms),
    )


@router.get(
    "/{room_id}",
    response_model=ApiResponse[RoomResponse],
    summary="Get room by id",
    description="Return a single room record by UUID.",
)
def get_room(room_id: UUID, db: Session = Depends(get_db)) -> dict:
    service = RoomService(db)
    room = service.get_by_id(room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return make_api_response(data=room, message="Room retrieved successfully.")


@router.put(
    "/{room_id}",
    response_model=ApiResponse[RoomResponse],
    summary="Update room",
    description="Update an existing room record by UUID.",
)
def update_room(room_id: UUID, payload: RoomUpdate, db: Session = Depends(get_db)) -> dict:
    service = RoomService(db)
    room = service.get_by_id(room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    updates = payload.model_dump(exclude_unset=True)
    for k, v in updates.items():
        setattr(room, k, v)
    updated_room = service.update(room)
    return make_api_response(data=updated_room, message="Room updated successfully.")


@router.delete(
    "/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete room",
    description="Delete a room by UUID. Returns 204 No Content on success.",
)
def delete_room(room_id: UUID, db: Session = Depends(get_db)):
    service = RoomService(db)
    room = service.get_by_id(room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    service.delete(room)
    return None
