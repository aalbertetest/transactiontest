"""
Example workflows for the Python workflow engine.
"""

from __future__ import annotations

import time
from typing import Dict

from workflow.config import EngineConfig
from workflow.engine import WorkflowContext
from workflow.logging import configure_logging
from workflow.persistence import SQLitePersistence
from workflow.worker import Worker
from workflow.scheduler import Scheduler
from workflow.engine import WorkflowEngine, ActivityContext


def transfer_workflow(ctx: WorkflowContext, input_data: Dict[str, any]) -> Dict[str, any]:
    amount = input_data["amount"]
    from_acct = input_data["from"]
    to_acct = input_data["to"]
    # Activity calls are deterministic. The engine records their results in history.
    debit_result = ctx.run_activity(
        "debit_account",
        {"account_id": from_acct, "amount": amount},
        timeout_seconds=30,
        max_attempts=3,
        heartbeat_interval_seconds=2,
    )
    ctx.sleep(1.0)
    credit_result = ctx.run_activity(
        "credit_account",
        {"account_id": to_acct, "amount": amount},
        timeout_seconds=30,
        max_attempts=3,
        heartbeat_interval_seconds=2,
    )
    return {"debit": debit_result, "credit": credit_result}


def debit_account(ctx: ActivityContext, input_data: Dict[str, any]) -> Dict[str, any]:
    # Simulate a slow operation with heartbeats.
    for idx in range(3):
        ctx.heartbeat({"step": idx})
        time.sleep(0.5)
    return {"status": "debited", "account": input_data["account_id"], "amount": input_data["amount"]}


def credit_account(ctx: ActivityContext, input_data: Dict[str, any]) -> Dict[str, any]:
    for idx in range(2):
        ctx.heartbeat({"step": idx})
        time.sleep(0.5)
    return {"status": "credited", "account": input_data["account_id"], "amount": input_data["amount"]}


def main() -> None:
    configure_logging("INFO")
    config = EngineConfig(db_path="workflow.db")
    persistence = SQLitePersistence(config.db_path)
    engine = WorkflowEngine(config, persistence)

    engine.register_workflow("transfer_workflow", transfer_workflow)
    engine.register_activity("debit_account", debit_account)
    engine.register_activity("credit_account", credit_account)

    worker = Worker(engine, config)
    scheduler = Scheduler(engine, config)

    worker_stop = worker.start_in_thread()
    scheduler_stop = scheduler.start_in_thread()

    execution = engine.start_workflow(
        "transfer_workflow",
        {"workflow_id": "transfer-001", "amount": 100, "from": "A", "to": "B"},
    )
    print(f"Started workflow {execution.workflow_id}/{execution.run_id}")

    # Let the workflow run.
    time.sleep(5)

    # Stop background loops.
    worker_stop.set()
    scheduler_stop.set()
    time.sleep(1)


if __name__ == "__main__":
    main()
