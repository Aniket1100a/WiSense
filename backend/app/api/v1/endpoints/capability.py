from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.capability import Capability
from app.schemas.capability import CapabilityCreate, CapabilityResponse, CapabilityUpdate
from app.services.capability_service import CapabilityService

router = APIRouter(prefix="/capabilities", tags=["Capabilities"])


@router.post("/", response_model=CapabilityResponse, status_code=status.HTTP_201_CREATED)
def create_capability(payload: CapabilityCreate, db: Session = Depends(get_db)) -> Capability:
    service = CapabilityService(db)
    capability = Capability(**payload.model_dump())
    return service.create(capability)


@router.get("/", response_model=List[CapabilityResponse])
def list_capabilities(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    service = CapabilityService(db)
    return service.list(limit=limit, offset=offset)


@router.get("/{capability_id}", response_model=CapabilityResponse)
def get_capability(capability_id: UUID, db: Session = Depends(get_db)):
    service = CapabilityService(db)
    cap = service.get_by_id(capability_id)
    if not cap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Capability not found")
    return cap


@router.put("/{capability_id}", response_model=CapabilityResponse)
def update_capability(capability_id: UUID, payload: CapabilityUpdate, db: Session = Depends(get_db)):
    service = CapabilityService(db)
    cap = service.get_by_id(capability_id)
    if not cap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Capability not found")
    updates = payload.model_dump(exclude_unset=True)
    for k, v in updates.items():
        setattr(cap, k, v)
    return service.update(cap)


@router.delete("/{capability_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_capability(capability_id: UUID, db: Session = Depends(get_db)):
    service = CapabilityService(db)
    cap = service.get_by_id(capability_id)
    if not cap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Capability not found")
    service.delete(cap)
    return None
