"""
Workflow state machine with validation.
"""

from __future__ import annotations

from typing import Dict, Set

from .types import WorkflowState


ALLOWED_TRANSITIONS: Dict[WorkflowState, Set[WorkflowState]] = {
    WorkflowState.CREATED: {WorkflowState.RUNNING, WorkflowState.CANCELED, WorkflowState.TERMINATED},
    WorkflowState.RUNNING: {
        WorkflowState.COMPLETED,
        WorkflowState.FAILED,
        WorkflowState.TIMED_OUT,
        WorkflowState.CANCELED,
        WorkflowState.TERMINATED,
    },
    WorkflowState.COMPLETED: set(),
    WorkflowState.FAILED: set(),
    WorkflowState.TIMED_OUT: set(),
    WorkflowState.CANCELED: set(),
    WorkflowState.TERMINATED: set(),
}


def validate_transition(current: WorkflowState, target: WorkflowState) -> None:
    if target not in ALLOWED_TRANSITIONS.get(current, set()):
        raise ValueError(f"Invalid workflow transition {current} -> {target}")
