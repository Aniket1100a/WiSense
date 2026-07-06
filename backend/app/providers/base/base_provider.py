from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseSensorProvider(ABC):
    """Abstract base class for sensor providers.

    Implementations should provide provider-specific logic. Placeholder
    implementations in this repo intentionally avoid hardware communication
    and either raise NotImplementedError (where appropriate) or return
    mocked information.
    """

    def __init__(self, sensor_info: Optional[Dict[str, Any]] = None) -> None:
        self.sensor_info = sensor_info or {}

    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def disconnect(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def discover(self) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    @abstractmethod
    def register(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @abstractmethod
    def heartbeat(self, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        raise NotImplementedError()

    @abstractmethod
    def health(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @abstractmethod
    def start_capture(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def stop_capture(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_capabilities(self) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    @abstractmethod
    def get_information(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        raise NotImplementedError()
