"""
Unit tests for the Python workflow engine.
"""

from __future__ import annotations

import tempfile
import time
import unittest

from workflow.backoff import compute_backoff_seconds
from workflow.config import EngineConfig
from workflow.engine import WorkflowEngine, WorkflowContext, ActivityContext
from workflow.persistence import SQLitePersistence
from workflow.scheduler import Scheduler
from workflow.worker import Worker
from workflow.types import WorkflowState


class BackoffTests(unittest.TestCase):
    def test_backoff_increases(self) -> None:
        first = compute_backoff_seconds(1, 1.0, 10.0, 0.0)
        second = compute_backoff_seconds(2, 1.0, 10.0, 0.0)
        third = compute_backoff_seconds(3, 1.0, 10.0, 0.0)
        self.assertEqual(first, 1.0)
        self.assertEqual(second, 2.0)
        self.assertEqual(third, 4.0)


class EngineIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.config = EngineConfig(
            db_path=self.tmp.name,
            worker_poll_interval_seconds=0.05,
            scheduler_poll_interval_seconds=0.05,
            lease_seconds=5,
        )
        self.persistence = SQLitePersistence(self.config.db_path)
        self.engine = WorkflowEngine(self.config, self.persistence)

    def tearDown(self) -> None:
        self.tmp.close()

    def test_workflow_end_to_end(self) -> None:
        def workflow(ctx: WorkflowContext, input_data: dict) -> dict:
            ctx.sleep(0.1)
            result = ctx.run_activity("echo", {"value": input_data["value"]})
            return {"result": result}

        def echo(ctx: ActivityContext, input_data: dict) -> dict:
            return {"echo": input_data["value"]}

        self.engine.register_workflow("test_workflow", workflow)
        self.engine.register_activity("echo", echo)

        worker = Worker(self.engine, self.config)
        scheduler = Scheduler(self.engine, self.config)
        worker_stop = worker.start_in_thread()
        scheduler_stop = scheduler.start_in_thread()

        execution = self.engine.start_workflow("test_workflow", {"value": "hello"})

        # Wait for completion with a timeout.
        deadline = time.time() + 5
        while time.time() < deadline:
            current = self.persistence.get_workflow_execution(execution.workflow_id, execution.run_id)
            if current.state == WorkflowState.COMPLETED:
                break
            time.sleep(0.1)

        worker_stop.set()
        scheduler_stop.set()
        time.sleep(0.2)

        final = self.persistence.get_workflow_execution(execution.workflow_id, execution.run_id)
        self.assertEqual(final.state, WorkflowState.COMPLETED)


if __name__ == "__main__":
    unittest.main()
