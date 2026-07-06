from __future__ import annotations

import enum
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.base import Base


class ProviderEnum(str, enum.Enum):
    esp32 = "esp32"
    windows_wifi = "windows_wifi"
    linux_wifi = "linux_wifi"
    usb_adapter = "usb_adapter"
    intel_csi = "intel_csi"
    dataset = "dataset"
    simulator = "simulator"


class SensorTypeEnum(str, enum.Enum):
    wifi = "WiFi"
    csi = "CSI"
    rssi = "RSSI"
    hybrid = "Hybrid"


class SensorStatusEnum(str, enum.Enum):
    online = "ONLINE"
    offline = "OFFLINE"
    connecting = "CONNECTING"
    error = "ERROR"
    disabled = "DISABLED"


class Sensor(Base):
    """Generic sensor device model supporting multiple hardware providers."""

    __tablename__ = "sensors"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    provider: Mapped[ProviderEnum] = mapped_column(Enum(ProviderEnum), nullable=False)
    sensor_type: Mapped[SensorTypeEnum] = mapped_column(
        Enum(SensorTypeEnum), nullable=False
    )
    status: Mapped[SensorStatusEnum] = mapped_column(
        Enum(SensorStatusEnum), nullable=False, default=SensorStatusEnum.offline
    )
    firmware_version: Mapped[str | None] = mapped_column(String(100), nullable=True)
    hardware_version: Mapped[str | None] = mapped_column(String(100), nullable=True)
    serial_number: Mapped[str | None] = mapped_column(String(200), nullable=True, unique=True)
    mac_address: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    ip_address: Mapped[str | None] = mapped_column(String(100), nullable=True)
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    room_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("rooms.id"), nullable=True
    )
    last_seen: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    meta: Mapped[str | None] = mapped_column("metadata", String, nullable=True)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    room = relationship("Room", back_populates="sensors", lazy="select")
    capabilities = relationship(
        "Capability", back_populates="sensor", cascade="all, delete-orphan", lazy="select"
    )
    signal_samples = relationship(
        "SignalSample", back_populates="sensor", cascade="all, delete-orphan", lazy="select"
    )
    activity_logs = relationship(
        "ActivityLog", back_populates="sensor", cascade="all, delete-orphan", lazy="select"
    )


Index("ix_sensors_mac_address", "mac_address")
