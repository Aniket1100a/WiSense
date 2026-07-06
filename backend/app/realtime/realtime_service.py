from typing import Any, Dict, Optional

from app.realtime.connection_manager import ConnectionManager
from app.realtime.event_bus import EventBus
from app.realtime.notification_manager import NotificationManager


class RealtimeService:
    """Encapsulates future realtime workflow and event propagation."""

    def __init__(self) -> None:
        self.connections = ConnectionManager()
        self.event_bus = EventBus()
        self.notifications = NotificationManager()

    def get_connection_manager(self) -> ConnectionManager:
        return self.connections

    def get_event_bus(self) -> EventBus:
        return self.event_bus

    def get_notification_manager(self) -> NotificationManager:
        return self.notifications

    def publish_event(self, event_name: str, payload: Dict[str, Any]) -> None:
        self.event_bus.publish(event_name, payload)

    def notify(self, recipient_id: str, payload: Dict[str, Any]) -> None:
        self.notifications.send(recipient_id, payload)

    def connect(self, connection_id: str, connection: Any) -> None:
        self.connections.connect(connection_id, connection)

    def disconnect(self, connection_id: str) -> None:
        self.connections.disconnect(connection_id)
