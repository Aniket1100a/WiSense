from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic import ConfigDict


class RoomBase(BaseModel):
    name: str = Field(..., max_length=200)
    building: Optional[str] = None
    floor: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class RoomCreate(RoomBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Main Lab",
                "building": "Research Center",
                "floor": "2",
                "description": "Room used for sensor testing and validation.",
            }
        },
    )


class RoomUpdate(BaseModel):
    name: Optional[str] = None
    building: Optional[str] = None
    floor: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Main Lab Updated",
                "description": "Updated room description.",
            }
        },
    )


class RoomResponse(RoomBase):
    id: UUID
    created_at: Optional[str]
    updated_at: Optional[str]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "00000000-0000-0000-0000-000000000000",
                "name": "Main Lab",
                "building": "Research Center",
                "floor": "2",
                "description": "Room used for sensor testing and validation.",
                "created_at": "2026-07-06T12:00:00Z",
                "updated_at": "2026-07-06T12:00:00Z",
            }
        },
    )
