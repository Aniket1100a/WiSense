from typing import Callable, Dict, List


class EventBus:
    """Event bus abstraction for publishing realtime events internally."""

    def __init__(self) -> None:
        self.handlers: Dict[str, List[Callable[..., None]]] = {}

    def subscribe(self, event_name: str, handler: Callable[..., None]) -> None:
        self.handlers.setdefault(event_name, []).append(handler)

    def publish(self, event_name: str, payload: dict) -> None:
        for handler in self.handlers.get(event_name, []):
            handler(payload)
