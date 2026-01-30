"""
Custom exceptions used by the workflow engine for control flow.
"""

from __future__ import annotations


class WorkflowApplicationError(Exception):
    """
    Raised when workflow or activity code fails.
    """


class PendingActivity(Exception):
    """
    Raised to suspend workflow execution until an activity completes.
    """

    def __init__(self, activity_id: str) -> None:
        super().__init__(f"Pending activity {activity_id}")
        self.activity_id = activity_id


class PendingTimer(Exception):
    """
    Raised to suspend workflow execution until a timer fires.
    """

    def __init__(self, timer_id: str) -> None:
        super().__init__(f"Pending timer {timer_id}")
        self.timer_id = timer_id


class DeterminismError(Exception):
    """
    Raised when workflow code behaves non-deterministically on replay.
    """
