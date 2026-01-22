from __future__ import annotations

from typing import Any, Callable, Dict, List


class PubSub:
    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable[[Any], None]]] = {}

    def subscribe(self, channel: str, handler: Callable[[Any], None]) -> Callable[[], None]:
        handlers = self._subscribers.setdefault(channel, [])
        handlers.append(handler)

        def unsubscribe() -> None:
            handlers = self._subscribers.get(channel, [])
            if handler in handlers:
                handlers.remove(handler)

        return unsubscribe

    def publish(self, channel: str, payload: Any) -> int:
        handlers = list(self._subscribers.get(channel, []))
        for handler in handlers:
            handler(payload)
        return len(handlers)
