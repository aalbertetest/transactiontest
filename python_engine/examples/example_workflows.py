"""
Example workflows and activities using the engine.
"""

from __future__ import annotations

import time
from typing import Any, Dict

from workflow_engine.config import EngineConfig
from workflow_engine.engine import WorkflowEngine
from workflow_engine.logging_utils import configure_logging
from workflow_engine.models import RetryPolicy
from workflow_engine.workflow import DecisionResult, ScheduleActivity, ScheduleTimer, WorkflowContext, WorkflowDefinition
from workflow_engine.worker import ActivityWorker, TimerWorker, WorkflowWorker
from workflow_engine.scheduler import Scheduler


class OrderWorkflow(WorkflowDefinition):
    name = "order-workflow"

    def initial_state(self) -> str:
        return "START"

    def decide(self, ctx: WorkflowContext, state: str, state_data: Dict[str, Any], history):
        commands = []
        if state == "START":
            activity_id = ctx.ensure_command_id("activity", "validate_activity_id")
            if ctx.activity_completed(activity_id):
                state = "VALIDATED"
            else:
                command_id = ctx.ensure_command_id("cmd", "validate_cmd")
                commands.append(
                    ScheduleActivity(
                        command_id=command_id,
                        activity_id=activity_id,
                        activity_name="validate_order",
                        input=ctx.workflow_input(),
                        timeout_seconds=10,
                        heartbeat_timeout_seconds=5,
                        retry_policy=RetryPolicy(),
                    )
                )
                return DecisionResult(next_state="WAIT_VALIDATE", state_data=state_data, commands=commands)

        if state == "WAIT_VALIDATE" or state == "VALIDATED":
            activity_id = state_data.get("validate_activity_id")
            if activity_id and not ctx.activity_completed(activity_id):
                return DecisionResult(next_state="WAIT_VALIDATE", state_data=state_data, commands=[])
            state = "CHARGE"

        if state == "CHARGE":
            activity_id = ctx.ensure_command_id("activity", "charge_activity_id")
            if ctx.activity_completed(activity_id):
                state = "CHARGED"
            else:
                command_id = ctx.ensure_command_id("cmd", "charge_cmd")
                commands.append(
                    ScheduleActivity(
                        command_id=command_id,
                        activity_id=activity_id,
                        activity_name="charge_card",
                        input={"amount": ctx.workflow_input().get("amount", 0)},
                        timeout_seconds=10,
                        heartbeat_timeout_seconds=5,
                        retry_policy=RetryPolicy(),
                    )
                )
                return DecisionResult(next_state="WAIT_CHARGE", state_data=state_data, commands=commands)

        if state in ("WAIT_CHARGE", "CHARGED"):
            activity_id = state_data.get("charge_activity_id")
            if activity_id and not ctx.activity_completed(activity_id):
                return DecisionResult(next_state="WAIT_CHARGE", state_data=state_data, commands=[])
            state = "SLEEP"

        if state == "SLEEP":
            timer_id = ctx.ensure_command_id("timer", "receipt_timer_id")
            if ctx.timer_fired(timer_id):
                state = "SEND_RECEIPT"
            else:
                command_id = ctx.ensure_command_id("cmd", "sleep_cmd")
                commands.append(ScheduleTimer(command_id=command_id, timer_id=timer_id, timeout_seconds=1))
                return DecisionResult(next_state="WAIT_TIMER", state_data=state_data, commands=commands)

        if state == "WAIT_TIMER":
            timer_id = state_data.get("receipt_timer_id")
            if timer_id and not ctx.timer_fired(timer_id):
                return DecisionResult(next_state="WAIT_TIMER", state_data=state_data, commands=[])
            state = "SEND_RECEIPT"

        if state == "SEND_RECEIPT":
            activity_id = ctx.ensure_command_id("activity", "receipt_activity_id")
            if ctx.activity_completed(activity_id):
                return DecisionResult(next_state="DONE", state_data=state_data, commands=[], complete=True)
            command_id = ctx.ensure_command_id("cmd", "receipt_cmd")
            commands.append(
                ScheduleActivity(
                    command_id=command_id,
                    activity_id=activity_id,
                    activity_name="send_receipt",
                    input={"email": ctx.workflow_input().get("email", "")},
                    timeout_seconds=10,
                    heartbeat_timeout_seconds=5,
                    retry_policy=RetryPolicy(),
                )
            )
            return DecisionResult(next_state="WAIT_RECEIPT", state_data=state_data, commands=commands)

        if state == "WAIT_RECEIPT":
            activity_id = state_data.get("receipt_activity_id")
            if activity_id and not ctx.activity_completed(activity_id):
                return DecisionResult(next_state="WAIT_RECEIPT", state_data=state_data, commands=[])
            return DecisionResult(next_state="DONE", state_data=state_data, commands=[], complete=True)

        return DecisionResult(next_state=state, state_data=state_data, commands=[])


def validate_order(ctx, payload: Dict[str, Any]) -> Dict[str, Any]:
    ctx.heartbeat()
    return {"valid": True, "order_id": payload.get("order_id", "unknown")}


def charge_card(ctx, payload: Dict[str, Any]) -> Dict[str, Any]:
    ctx.heartbeat()
    return {"charged": True, "amount": payload.get("amount", 0)}


def send_receipt(ctx, payload: Dict[str, Any]) -> Dict[str, Any]:
    ctx.heartbeat()
    return {"sent": True, "email": payload.get("email", "")}


def main() -> None:
    configure_logging("INFO")
    config = EngineConfig(db_path="example_engine.sqlite")
    engine = WorkflowEngine(config)
    engine.register_workflow(OrderWorkflow())
    engine.register_activity("validate_order", validate_order)
    engine.register_activity("charge_card", charge_card)
    engine.register_activity("send_receipt", send_receipt)

    scheduler = Scheduler(engine)
    workflow_worker = WorkflowWorker("workflow-worker", engine)
    activity_worker = ActivityWorker("activity-worker", engine, concurrency=2)
    timer_worker = TimerWorker("timer-worker", engine)

    scheduler.start()
    workflow_worker.start()
    activity_worker.start()
    timer_worker.start()

    run_id = engine.start_workflow(
        workflow_type="order-workflow",
        workflow_id="order-123",
        input_payload={"order_id": "order-123", "amount": 25, "email": "user@example.com"},
    )
    print(f"Started run {run_id}")

    while True:
        run = engine.persistence.get_run(run_id)
        if run and run["status"] in ("COMPLETED", "FAILED"):
            print("Workflow completed with status", run["status"])
            break
        time.sleep(0.5)

    scheduler.stop()
    workflow_worker.stop()
    activity_worker.stop()
    timer_worker.stop()


if __name__ == "__main__":
    main()
