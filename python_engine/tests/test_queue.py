import tempfile
import time
import unittest

from workflow_engine.config import EngineConfig
from workflow_engine.engine import WorkflowEngine


class QueueTests(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        config = EngineConfig(db_path=self.temp_db.name)
        self.engine = WorkflowEngine(config)

    def tearDown(self):
        try:
            import os

            os.unlink(self.temp_db.name)
        except Exception:
            pass

    def test_enqueue_and_lease(self):
        task_id = self.engine.queue.enqueue_task(
            run_id="run-1",
            task_type="workflow_task",
            queue_name=self.engine.config.workflow_task_queue,
            payload={"run_id": "run-1"},
            timeout_seconds=10,
            max_attempts=2,
        )
        tasks = self.engine.queue.lease_tasks(
            self.engine.config.workflow_task_queue, limit=1, lease_seconds=5
        )
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].task_id, task_id)
        self.engine.queue.complete_task(task_id)

    def test_reschedule(self):
        task_id = self.engine.queue.enqueue_task(
            run_id="run-1",
            task_type="timer_task",
            queue_name=self.engine.config.timer_task_queue,
            payload={"run_id": "run-1", "timer_id": "t1"},
            scheduled_at=time.time() + 1.0,
            max_attempts=1,
        )
        tasks = self.engine.queue.lease_tasks(
            self.engine.config.timer_task_queue, limit=1, lease_seconds=5
        )
        self.assertEqual(len(tasks), 0)
        self.engine.queue.reschedule_task(task_id, scheduled_at=time.time() - 1.0)
        tasks = self.engine.queue.lease_tasks(
            self.engine.config.timer_task_queue, limit=1, lease_seconds=5
        )
        self.assertEqual(len(tasks), 1)


if __name__ == "__main__":
    unittest.main()
