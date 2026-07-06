from __future__ import annotations

import uuid
from sqlalchemy import DateTime, Float, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.base import Base


class SignalSample(Base):
    """Represents a single captured signal sample from a sensor."""

    __tablename__ = "signal_samples"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    rssi: Mapped[float | None] = mapped_column(Float, nullable=True)
    channel: Mapped[int | None] = mapped_column(Integer, nullable=True)
    frequency: Mapped[int | None] = mapped_column(Integer, nullable=True)
    noise: Mapped[float | None] = mapped_column(Float, nullable=True)
    snr: Mapped[float | None] = mapped_column(Float, nullable=True)
    raw_payload: Mapped[dict | None] = mapped_column(String, nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    sensor = relationship("Sensor", back_populates="signal_samples", lazy="select", primaryjoin="SignalSample.sensor_id==Sensor.id")
