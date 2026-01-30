import os
import tempfile
import unittest

from engine import DBTaskQueue, SQLiteStore


class TaskQueueTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(prefix="queue-test-", suffix=".db")
        self.store = SQLiteStore(self.db_path)
        self.queue = DBTaskQueue(self.store.connection)

    def tearDown(self):
        os.close(self.db_fd)
        os.remove(self.db_path)

    def test_enqueue_poll_ack(self):
        task_id = self.queue.enqueue(
            queue_name="default",
            task_type="workflow",
            payload={"workflow_id": "wf1"},
        )
        self.assertIsNotNone(task_id)

        task = self.queue.poll(
            queue_name="default",
            task_type="workflow",
            lease_duration_seconds=5,
            worker_id="worker-1",
        )
        self.assertIsNotNone(task)
        self.assertEqual(task.payload["workflow_id"], "wf1")

        self.queue.ack(task.id)
        task = self.queue.poll(
            queue_name="default",
            task_type="workflow",
            lease_duration_seconds=5,
            worker_id="worker-1",
        )
        self.assertIsNone(task)


if __name__ == "__main__":
    unittest.main()

