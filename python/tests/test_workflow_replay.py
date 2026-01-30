import unittest

from engine.runtime import WorkflowRunner
from engine.models import (
    EVENT_ACTIVITY_TASK_COMPLETED,
    EVENT_ACTIVITY_TASK_SCHEDULED,
    EVENT_SIGNAL_RECEIVED,
    EVENT_TIMER_FIRED,
    EVENT_TIMER_SCHEDULED,
    HistoryEvent,
    RetryPolicy,
)


def sample_workflow(ctx, input_payload):
    greeting = yield ctx.execute_activity("compose", {"name": input_payload["name"]})
    yield ctx.sleep(1)
    approval = yield ctx.wait_signal("approve")
    return {"greeting": greeting, "approved_by": approval["user"]}


class WorkflowReplayTestCase(unittest.TestCase):
    def test_replay_completes(self):
        history = [
            HistoryEvent(
                event_id=1,
                event_type=EVENT_ACTIVITY_TASK_SCHEDULED,
                event_time=1,
                attributes={
                    "activity_id": "activity-1",
                    "activity_name": "compose",
                    "input": {"name": "Ada"},
                },
            ),
            HistoryEvent(
                event_id=2,
                event_type=EVENT_ACTIVITY_TASK_COMPLETED,
                event_time=2,
                attributes={"activity_id": "activity-1", "result": "Hello, Ada"},
            ),
            HistoryEvent(
                event_id=3,
                event_type=EVENT_TIMER_SCHEDULED,
                event_time=3,
                attributes={"timer_id": "timer-1", "fire_at": 10},
            ),
            HistoryEvent(
                event_id=4,
                event_type=EVENT_TIMER_FIRED,
                event_time=4,
                attributes={"timer_id": "timer-1"},
            ),
            HistoryEvent(
                event_id=5,
                event_type=EVENT_SIGNAL_RECEIVED,
                event_time=5,
                attributes={"signal_name": "approve", "payload": {"user": "bob"}},
            ),
        ]
        runner = WorkflowRunner(
            workflow_func=sample_workflow,
            input_payload={"name": "Ada"},
            history=history,
            default_retry_policy=RetryPolicy(
                initial_interval_seconds=1,
                max_interval_seconds=10,
                backoff_coefficient=2.0,
                max_attempts=3,
            ),
        )
        result = runner.run()
        self.assertEqual(result.status, "COMPLETED")
        self.assertEqual(result.result["greeting"], "Hello, Ada")
        self.assertEqual(result.result["approved_by"], "bob")


if __name__ == "__main__":
    unittest.main()

