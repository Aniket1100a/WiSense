from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.common import make_api_response, make_paginated_response
from app.database.session import get_db
from app.models.capability import Capability
from app.schemas.capability import CapabilityCreate, CapabilityResponse, CapabilityUpdate
from app.schemas.response import ApiResponse
from app.services.capability_service import CapabilityService

router = APIRouter(prefix="/capabilities", tags=["Capabilities"])


@router.post(
    "/",
    response_model=ApiResponse[CapabilityResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a capability",
    description="Create a new capability associated with a sensor.",
)
def create_capability(payload: CapabilityCreate, db: Session = Depends(get_db)) -> dict:
    service = CapabilityService(db)
    capability = Capability(**payload.model_dump())
    created_capability = service.create(capability)
    return make_api_response(data=created_capability, message="Capability created successfully.")


@router.get(
    "/",
    response_model=ApiResponse[List[CapabilityResponse]],
    summary="List capabilities",
    description="Return a paginated list of sensor capabilities.",
)
def list_capabilities(
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
    service = CapabilityService(db)
    capabilities = service.list(limit=limit, offset=offset)
    return make_paginated_response(
        data=capabilities,
        message="Capabilities retrieved successfully.",
        limit=limit,
        offset=offset,
        count=len(capabilities),
    )


@router.get(
    "/{capability_id}",
    response_model=ApiResponse[CapabilityResponse],
    summary="Get capability by id",
    description="Return a single capability by UUID.",
)
def get_capability(capability_id: UUID, db: Session = Depends(get_db)) -> dict:
    service = CapabilityService(db)
    cap = service.get_by_id(capability_id)
    if not cap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Capability not found")
    return make_api_response(data=cap, message="Capability retrieved successfully.")


@router.put(
    "/{capability_id}",
    response_model=ApiResponse[CapabilityResponse],
    summary="Update capability",
    description="Update an existing capability by UUID.",
)
def update_capability(capability_id: UUID, payload: CapabilityUpdate, db: Session = Depends(get_db)) -> dict:
    service = CapabilityService(db)
    cap = service.get_by_id(capability_id)
    if not cap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Capability not found")
    updates = payload.model_dump(exclude_unset=True)
    for k, v in updates.items():
        setattr(cap, k, v)
    updated_cap = service.update(cap)
    return make_api_response(data=updated_cap, message="Capability updated successfully.")


@router.delete(
    "/{capability_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete capability",
    description="Delete a capability by UUID. Returns 204 No Content on success.",
)
def delete_capability(capability_id: UUID, db: Session = Depends(get_db)):
    service = CapabilityService(db)
    cap = service.get_by_id(capability_id)
    if not cap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Capability not found")
    service.delete(cap)
    return None
