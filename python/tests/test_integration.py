import os
import tempfile
import time
import unittest

from engine import Config, DBTaskQueue, SQLiteStore, WorkflowEngine, Worker, TimerScheduler


def add_workflow(ctx, input_payload):
    result = yield ctx.execute_activity("add", {"a": input_payload["a"], "b": input_payload["b"]})
    return {"sum": result}


def add_activity(activity_ctx, input_payload):
    activity_ctx.heartbeat({"stage": "adding"})
    return input_payload["a"] + input_payload["b"]


class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(prefix="engine-test-", suffix=".db")
        self.config = Config(db_path=self.db_path, task_queue_name="default", worker_id="worker-test")
        self.store = SQLiteStore(self.config.db_path)
        self.queue = DBTaskQueue(self.store.connection)
        self.engine = WorkflowEngine(self.store, self.queue, self.config)
        self.worker = Worker(self.store, self.queue, self.config)
        self.worker.register_workflow("AddWorkflow", add_workflow)
        self.worker.register_activity("add", add_activity)
        self.scheduler = TimerScheduler(self.store, self.queue, self.config)

    def tearDown(self):
        os.close(self.db_fd)
        os.remove(self.db_path)

    def test_workflow_executes(self):
        run_id = self.engine.start_workflow(
            workflow_id="add-workflow-1",
            workflow_type="AddWorkflow",
            input_payload={"a": 2, "b": 3},
        )
        for _ in range(50):
            self.worker.run_once()
            self.scheduler.run_once()
            execution = self.store.get_workflow_execution("add-workflow-1", run_id)
            if execution and execution["state"] == "COMPLETED":
                break
            time.sleep(0.05)
        execution = self.store.get_workflow_execution("add-workflow-1", run_id)
        self.assertIsNotNone(execution)
        self.assertEqual(execution["state"], "COMPLETED")
        self.assertIn("sum", execution["result"])


if __name__ == "__main__":
    unittest.main()

