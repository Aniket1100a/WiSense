from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.capability import Capability


class CapabilityRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, capability: Capability) -> Capability:
        self.session.add(capability)
        self.session.commit()
        self.session.refresh(capability)
        return capability

    def update(self, capability: Capability) -> Capability:
        self.session.add(capability)
        self.session.commit()
        self.session.refresh(capability)
        return capability

    def delete(self, capability: Capability) -> None:
        self.session.delete(capability)
        self.session.commit()

    def get_by_id(self, id: UUID) -> Optional[Capability]:
        return self.session.get(Capability, id)

    def get_all(self, limit: int = 100, offset: int = 0) -> List[Capability]:
        stmt = select(Capability).limit(limit).offset(offset)
        return list(self.session.scalars(stmt))
