from __future__ import annotations

from typing import Iterable, Optional

from .transport import ReplicationMessage, Transport


class Replicator:
    def __init__(self, transport: Optional[Transport] = None) -> None:
        self._transport = transport

    def replicate(self, peer_ids: Iterable[str], message: ReplicationMessage) -> None:
        if not self._transport:
            return
        for peer_id in peer_ids:
            self._transport.send(peer_id, message)
