from typing import Any, Dict, List, Optional


class NotificationManager:
    """Manages notifications for realtime delivery and history."""

    def __init__(self) -> None:
        self.notifications: List[Dict[str, Any]] = []

    def send(self, recipient_id: str, payload: Dict[str, Any]) -> None:
        self.notifications.append({"recipient_id": recipient_id, "payload": payload})

    def list_notifications(self, recipient_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if recipient_id is None:
            return self.notifications
        return [item for item in self.notifications if item["recipient_id"] == recipient_id]
