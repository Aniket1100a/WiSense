from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.capability import Capability
from app.repositories.capability_repository import CapabilityRepository


class CapabilityService:
    def __init__(self, session: Session) -> None:
        self.repo = CapabilityRepository(session)

    def create(self, capability: Capability) -> Capability:
        return self.repo.create(capability)

    def update(self, capability: Capability) -> Capability:
        return self.repo.update(capability)

    def delete(self, capability: Capability) -> None:
        return self.repo.delete(capability)

    def get_by_id(self, id: UUID) -> Optional[Capability]:
        return self.repo.get_by_id(id)

    def list(self, limit: int = 100, offset: int = 0) -> List[Capability]:
        return self.repo.get_all(limit=limit, offset=offset)
