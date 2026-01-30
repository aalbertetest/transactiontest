"""
Timeout handling utilities.
"""

from __future__ import annotations

import time
from typing import Callable


class TimeoutManager:
    def __init__(self, on_task_timeout: Callable[[str], None], on_heartbeat_timeout: Callable[[str], None], on_run_timeout: Callable[[str], None]) -> None:
        self._on_task_timeout = on_task_timeout
        self._on_heartbeat_timeout = on_heartbeat_timeout
        self._on_run_timeout = on_run_timeout

    def sweep(
        self,
        task_timeout_ids: list[str],
        heartbeat_timeout_ids: list[str],
        run_timeout_ids: list[str],
    ) -> None:
        for task_id in task_timeout_ids:
            self._on_task_timeout(task_id)
        for task_id in heartbeat_timeout_ids:
            self._on_heartbeat_timeout(task_id)
        for run_id in run_timeout_ids:
            self._on_run_timeout(run_id)

    @staticmethod
    def now() -> float:
        return time.time()
