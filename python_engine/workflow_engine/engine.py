"""
Core workflow engine logic.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from .config import EngineConfig
from .logging_utils import get_logger
from .metrics import MetricsRegistry
from .models import HistoryEvent, RetryPolicy, Task
from .persistence import SqlitePersistence
from .queue import TaskQueue
from .retry import compute_backoff_seconds, should_retry
from .workflow import Command, DecisionResult, FailWorkflow, ScheduleActivity, ScheduleTimer, WorkflowContext, WorkflowDefinition


ActivityFunction = Callable[["ActivityContext", Dict[str, Any]], Dict[str, Any]]


@dataclass
class ActivityDefinition:
    name: str
    func: ActivityFunction
    retry_policy: RetryPolicy
    timeout_seconds: int
    heartbeat_timeout_seconds: int


class ActivityContext:
    def __init__(self, engine: "WorkflowEngine", task_id: str) -> None:
        self._engine = engine
        self._task_id = task_id

    def heartbeat(self) -> None:
        self._engine.queue.heartbeat(self._task_id)
        self._engine.metrics.counter("activity_heartbeats_total").inc()


class WorkflowEngine:
    def __init__(self, config: EngineConfig) -> None:
        self.config = config
        self.logger = get_logger("workflow_engine", level=config.log_level)
        self.persistence = SqlitePersistence(config.db_path)
        self.queue = TaskQueue(self.persistence)
        self.metrics = MetricsRegistry()
        self._workflows: Dict[str, WorkflowDefinition] = {}
        self._activities: Dict[str, ActivityDefinition] = {}

    def register_workflow(self, definition: WorkflowDefinition) -> None:
        self._workflows[definition.name] = definition

    def register_activity(
        self,
        name: str,
        func: ActivityFunction,
        retry_policy: Optional[RetryPolicy] = None,
        timeout_seconds: Optional[int] = None,
        heartbeat_timeout_seconds: Optional[int] = None,
    ) -> None:
        policy = retry_policy or RetryPolicy()
        self._activities[name] = ActivityDefinition(
            name=name,
            func=func,
            retry_policy=policy,
            timeout_seconds=timeout_seconds or self.config.workflow_task_timeout_seconds,
            heartbeat_timeout_seconds=heartbeat_timeout_seconds or self.config.activity_heartbeat_timeout_seconds,
        )

    def start_workflow(
        self,
        workflow_type: str,
        workflow_id: str,
        input_payload: Dict[str, Any],
        run_timeout_seconds: Optional[int] = None,
    ) -> str:
        if workflow_type not in self._workflows:
            raise ValueError(f"Unknown workflow type {workflow_type}")
        run_id = str(uuid.uuid4())
        definition = self._workflows[workflow_type]
        timeout = run_timeout_seconds or self.config.run_timeout_seconds
        self.persistence.create_run(
            workflow_id=workflow_id,
            workflow_type=workflow_type,
            run_id=run_id,
            state=definition.initial_state(),
            state_data={"sequence": 0},
            run_timeout_seconds=timeout,
            workflow_task_timeout_seconds=self.config.workflow_task_timeout_seconds,
            input_payload=input_payload,
        )
        self.enqueue_workflow_task(run_id)
        self.logger.info("Started workflow %s run %s", workflow_id, run_id)
        return run_id

    def enqueue_workflow_task(self, run_id: str) -> str:
        return self.queue.enqueue_task(
            run_id=run_id,
            task_type="workflow_task",
            queue_name=self.config.workflow_task_queue,
            payload={"run_id": run_id},
            timeout_seconds=self.config.workflow_task_timeout_seconds,
            max_attempts=self.config.max_task_attempts,
        )

    def enqueue_activity_task(self, run_id: str, activity_name: str, payload: Dict[str, Any], timeout_seconds: int, heartbeat_timeout_seconds: int, max_attempts: int) -> str:
        return self.queue.enqueue_task(
            run_id=run_id,
            task_type="activity_task",
            queue_name=self.config.activity_task_queue,
            payload=payload,
            timeout_seconds=timeout_seconds,
            heartbeat_timeout_seconds=heartbeat_timeout_seconds,
            max_attempts=max_attempts,
        )

    def enqueue_timer_task(self, run_id: str, payload: Dict[str, Any], fire_at: float) -> str:
        return self.queue.enqueue_task(
            run_id=run_id,
            task_type="timer_task",
            queue_name=self.config.timer_task_queue,
            payload=payload,
            scheduled_at=fire_at,
            timeout_seconds=None,
            max_attempts=self.config.max_task_attempts,
        )

    def process_workflow_task(self, task: Task) -> None:
        run_id = task.payload["run_id"]
        run = self.persistence.get_run(run_id)
        if not run or run["status"] != "RUNNING":
            self.queue.complete_task(task.task_id)
            return

        self.persistence.append_event(run_id, "WorkflowTaskStarted", {"task_id": task.task_id})
        history = self.persistence.list_events(run_id)
        definition = self._workflows[run["workflow_type"]]
        ctx = WorkflowContext(run_id, run["state_data"], history)
        decision = definition.decide(ctx, run["state"], ctx.state_data, history)

        self._apply_decision(run_id, decision, history)
        self.queue.complete_task(task.task_id)
        self.metrics.counter("workflow_tasks_completed_total").inc()

    def _apply_decision(self, run_id: str, decision: DecisionResult, history: List[HistoryEvent]) -> None:
        status = "RUNNING"
        terminal_from_command: Optional[str] = None
        for command in decision.commands:
            self._apply_command(run_id, command, history)
            if command.command_type == "CompleteWorkflow":
                terminal_from_command = "COMPLETED"
            if command.command_type == "FailWorkflow":
                terminal_from_command = "FAILED"

        if terminal_from_command:
            status = terminal_from_command
        elif decision.complete:
            status = "COMPLETED"
            self.persistence.append_event(run_id, "WorkflowCompleted", {"result": {"status": "completed"}})
        elif decision.failure:
            status = "FAILED"
            self.persistence.append_event(run_id, "WorkflowFailed", {"error": decision.failure})

        self.persistence.update_run_state(run_id, decision.next_state, decision.state_data, status=status)
        self.persistence.append_event(
            run_id,
            "WorkflowTaskCompleted",
            {"state": decision.next_state, "commands": [cmd.command_type for cmd in decision.commands]},
        )

    def _apply_command(self, run_id: str, command: Command, history: List[HistoryEvent]) -> None:
        if command.command_type == "ScheduleActivity":
            self._apply_schedule_activity(run_id, command, history)
        elif command.command_type == "ScheduleTimer":
            self._apply_schedule_timer(run_id, command, history)
        elif command.command_type == "CompleteWorkflow":
            self.persistence.append_event(run_id, "WorkflowCompleted", {"result": command.attributes["result"]})
        elif command.command_type == "FailWorkflow":
            self.persistence.append_event(run_id, "WorkflowFailed", {"error": command.attributes["error"]})

    def _history_has_command(self, history: List[HistoryEvent], event_type: str, command_id: str) -> bool:
        return any(
            event.event_type == event_type and event.attributes.get("command_id") == command_id
            for event in history
        )

    def _apply_schedule_activity(self, run_id: str, command: Command, history: List[HistoryEvent]) -> None:
        command_id = command.attributes.get("command_id")
        if not command_id:
            raise ValueError("ScheduleActivity requires command_id for determinism")
        if self._history_has_command(history, "ActivityScheduled", command_id):
            return

        activity_name = command.attributes["activity_name"]
        if activity_name not in self._activities:
            raise ValueError(f"Unknown activity {activity_name}")
        activity_id = command.attributes["activity_id"]
        input_payload = command.attributes["input"]
        retry_policy = RetryPolicy(**command.attributes["retry_policy"])
        timeout_seconds = int(command.attributes["timeout_seconds"])
        heartbeat_timeout_seconds = int(command.attributes["heartbeat_timeout_seconds"])

        self.persistence.append_event(
            run_id,
            "ActivityScheduled",
            {
                "command_id": command_id,
                "activity_id": activity_id,
                "activity_name": activity_name,
                "input": input_payload,
                "timeout_seconds": timeout_seconds,
                "heartbeat_timeout_seconds": heartbeat_timeout_seconds,
                "retry_policy": retry_policy.__dict__,
            },
        )
        self.enqueue_activity_task(
            run_id=run_id,
            activity_name=activity_name,
            payload={
                "run_id": run_id,
                "activity_id": activity_id,
                "activity_name": activity_name,
                "input": input_payload,
                "retry_policy": retry_policy.__dict__,
            },
            timeout_seconds=timeout_seconds,
            heartbeat_timeout_seconds=heartbeat_timeout_seconds,
            max_attempts=retry_policy.max_attempts,
        )

    def _apply_schedule_timer(self, run_id: str, command: Command, history: List[HistoryEvent]) -> None:
        command_id = command.attributes.get("command_id")
        if not command_id:
            raise ValueError("ScheduleTimer requires command_id for determinism")
        if self._history_has_command(history, "TimerScheduled", command_id):
            return
        timer_id = command.attributes["timer_id"]
        timeout_seconds = int(command.attributes["timeout_seconds"])
        fire_at = time.time() + timeout_seconds
        self.persistence.append_event(
            run_id,
            "TimerScheduled",
            {"command_id": command_id, "timer_id": timer_id, "fire_at": fire_at},
        )
        self.enqueue_timer_task(run_id, {"run_id": run_id, "timer_id": timer_id}, fire_at=fire_at)

    def record_activity_started(self, run_id: str, activity_id: str, task_id: str, attempt: int) -> None:
        self.persistence.append_event(
            run_id,
            "ActivityStarted",
            {"activity_id": activity_id, "task_id": task_id, "attempt": attempt},
        )

    def record_activity_completed(self, run_id: str, activity_id: str, result: Dict[str, Any], task_id: str, attempt: int) -> None:
        self.persistence.append_event(
            run_id,
            "ActivityCompleted",
            {"activity_id": activity_id, "result": result, "task_id": task_id, "attempt": attempt},
        )
        self.enqueue_workflow_task(run_id)

    def record_activity_failed(self, run_id: str, activity_id: str, error: str, task_id: str, attempt: int, retry_policy: RetryPolicy) -> None:
        self.persistence.append_event(
            run_id,
            "ActivityFailed",
            {"activity_id": activity_id, "error": error, "task_id": task_id, "attempt": attempt},
        )
        if should_retry(attempt, retry_policy):
            backoff = compute_backoff_seconds(attempt, retry_policy)
            scheduled_at = time.time() + backoff
            self.logger.warning("Retrying activity %s in %.2fs", activity_id, backoff)
            self.queue.reschedule_task(task_id, scheduled_at=scheduled_at)
            self.persistence.append_event(
                run_id,
                "ActivityRetryScheduled",
                {"activity_id": activity_id, "attempt": attempt + 1, "backoff_seconds": backoff},
            )
        else:
            self.enqueue_workflow_task(run_id)

    def record_timer_fired(self, run_id: str, timer_id: str) -> None:
        self.persistence.append_event(
            run_id,
            "TimerFired",
            {"timer_id": timer_id},
        )
        self.enqueue_workflow_task(run_id)

    def record_task_timeout(self, task_id: str) -> None:
        task = self.queue.get_task(task_id)
        if not task:
            return
        self.queue.fail_task(task_id, "timeout")
        if task.task_type == "activity_task":
            retry_policy = RetryPolicy(**task.payload.get("retry_policy", {}))
            self.record_activity_failed(
                run_id=task.run_id,
                activity_id=task.payload.get("activity_id", ""),
                error="timeout",
                task_id=task_id,
                attempt=task.attempt,
                retry_policy=retry_policy,
            )

    def record_heartbeat_timeout(self, task_id: str) -> None:
        task = self.queue.get_task(task_id)
        if not task:
            return
        self.queue.fail_task(task_id, "heartbeat_timeout")
        if task.task_type == "activity_task":
            retry_policy = RetryPolicy(**task.payload.get("retry_policy", {}))
            self.record_activity_failed(
                run_id=task.run_id,
                activity_id=task.payload.get("activity_id", ""),
                error="heartbeat_timeout",
                task_id=task_id,
                attempt=task.attempt,
                retry_policy=retry_policy,
            )

    def record_run_timeout(self, run_id: str) -> None:
        self.persistence.append_event(run_id, "WorkflowFailed", {"error": "run_timeout"})
        self.persistence.update_run_state(run_id, "FAILED", {}, status="FAILED")
