import tempfile
import time
import unittest
from typing import Any, Dict

from workflow_engine.config import EngineConfig
from workflow_engine.engine import WorkflowEngine
from workflow_engine.models import RetryPolicy
from workflow_engine.workflow import DecisionResult, ScheduleActivity, ScheduleTimer, WorkflowContext, WorkflowDefinition
from workflow_engine.worker import ActivityWorker, TimerWorker, WorkflowWorker
from workflow_engine.scheduler import Scheduler


class TimerWorkflow(WorkflowDefinition):
    name = "timer-workflow"

    def initial_state(self) -> str:
        return "START"

    def decide(self, ctx: WorkflowContext, state: str, state_data: Dict[str, Any], history):
        if state == "START":
            timer_id = ctx.ensure_command_id("timer", "timer_id")
            if ctx.timer_fired(timer_id):
                return DecisionResult(next_state="TIMER_DONE", state_data=state_data, commands=[])
            command_id = ctx.ensure_command_id("cmd", "timer_cmd")
            return DecisionResult(
                next_state="WAIT_TIMER",
                state_data=state_data,
                commands=[ScheduleTimer(command_id=command_id, timer_id=timer_id, timeout_seconds=1)],
            )
        if state == "WAIT_TIMER":
            timer_id = state_data.get("timer_id")
            if timer_id and not ctx.timer_fired(timer_id):
                return DecisionResult(next_state="WAIT_TIMER", state_data=state_data, commands=[])
            state = "TIMER_DONE"
        if state == "TIMER_DONE":
            activity_id = ctx.ensure_command_id("activity", "activity_id")
            if ctx.activity_completed(activity_id):
                return DecisionResult(next_state="DONE", state_data=state_data, commands=[], complete=True)
            command_id = ctx.ensure_command_id("cmd", "activity_cmd")
            return DecisionResult(
                next_state="WAIT_ACTIVITY",
                state_data=state_data,
                commands=[
                    ScheduleActivity(
                        command_id=command_id,
                        activity_id=activity_id,
                        activity_name="step",
                        input={"value": "integration"},
                        timeout_seconds=5,
                        heartbeat_timeout_seconds=2,
                        retry_policy=RetryPolicy(),
                    )
                ],
            )
        if state == "WAIT_ACTIVITY":
            activity_id = state_data.get("activity_id")
            if activity_id and ctx.activity_completed(activity_id):
                return DecisionResult(next_state="DONE", state_data=state_data, commands=[], complete=True)
            return DecisionResult(next_state="WAIT_ACTIVITY", state_data=state_data, commands=[])
        return DecisionResult(next_state=state, state_data=state_data, commands=[])


def step_activity(ctx, payload: Dict[str, Any]) -> Dict[str, Any]:
    ctx.heartbeat()
    return {"value": payload.get("value")}


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        config = EngineConfig(db_path=self.temp_db.name, worker_poll_interval_seconds=0.1)
        self.engine = WorkflowEngine(config)
        self.engine.register_workflow(TimerWorkflow())
        self.engine.register_activity("step", step_activity)

    def tearDown(self):
        try:
            import os

            os.unlink(self.temp_db.name)
        except Exception:
            pass

    def test_timer_workflow(self):
        scheduler = Scheduler(self.engine)
        workflow_worker = WorkflowWorker("workflow-worker", self.engine)
        activity_worker = ActivityWorker("activity-worker", self.engine)
        timer_worker = TimerWorker("timer-worker", self.engine)
        scheduler.start()
        workflow_worker.start()
        activity_worker.start()
        timer_worker.start()

        run_id = self.engine.start_workflow("timer-workflow", "wf-integration", {"input": "x"})
        deadline = time.time() + 10
        status = None
        while time.time() < deadline:
            run = self.engine.persistence.get_run(run_id)
            if run and run["status"] in ("COMPLETED", "FAILED"):
                status = run["status"]
                break
            time.sleep(0.1)
        scheduler.stop()
        workflow_worker.stop()
        activity_worker.stop()
        timer_worker.stop()
        self.assertEqual(status, "COMPLETED")


if __name__ == "__main__":
    unittest.main()
