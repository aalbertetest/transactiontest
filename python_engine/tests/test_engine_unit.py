import tempfile
import time
import unittest
from typing import Any, Dict

from workflow_engine.config import EngineConfig
from workflow_engine.engine import WorkflowEngine
from workflow_engine.models import RetryPolicy
from workflow_engine.workflow import DecisionResult, ScheduleActivity, WorkflowContext, WorkflowDefinition
from workflow_engine.worker import ActivityWorker, WorkflowWorker
from workflow_engine.scheduler import Scheduler


class SimpleWorkflow(WorkflowDefinition):
    name = "simple-workflow"

    def initial_state(self) -> str:
        return "START"

    def decide(self, ctx: WorkflowContext, state: str, state_data: Dict[str, Any], history):
        if state == "START":
            activity_id = ctx.ensure_command_id("activity", "hello_activity_id")
            if ctx.activity_completed(activity_id):
                return DecisionResult(next_state="DONE", state_data=state_data, commands=[], complete=True)
            command_id = ctx.ensure_command_id("cmd", "hello_cmd")
            return DecisionResult(
                next_state="WAIT_ACTIVITY",
                state_data=state_data,
                commands=[
                    ScheduleActivity(
                        command_id=command_id,
                        activity_id=activity_id,
                        activity_name="hello",
                        input={"name": "unit"},
                        timeout_seconds=5,
                        heartbeat_timeout_seconds=2,
                        retry_policy=RetryPolicy(),
                    )
                ],
            )
        if state == "WAIT_ACTIVITY":
            activity_id = state_data.get("hello_activity_id")
            if activity_id and ctx.activity_completed(activity_id):
                return DecisionResult(next_state="DONE", state_data=state_data, commands=[], complete=True)
            return DecisionResult(next_state="WAIT_ACTIVITY", state_data=state_data, commands=[])
        return DecisionResult(next_state=state, state_data=state_data, commands=[])


def hello_activity(ctx, payload: Dict[str, Any]) -> Dict[str, Any]:
    ctx.heartbeat()
    return {"message": f"hello {payload.get('name', '')}"}


class EngineUnitTests(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        config = EngineConfig(db_path=self.temp_db.name, worker_poll_interval_seconds=0.1)
        self.engine = WorkflowEngine(config)
        self.engine.register_workflow(SimpleWorkflow())
        self.engine.register_activity("hello", hello_activity)

    def tearDown(self):
        try:
            import os

            os.unlink(self.temp_db.name)
        except Exception:
            pass

    def test_workflow_completes(self):
        scheduler = Scheduler(self.engine)
        workflow_worker = WorkflowWorker("workflow-worker", self.engine)
        activity_worker = ActivityWorker("activity-worker", self.engine)
        scheduler.start()
        workflow_worker.start()
        activity_worker.start()

        run_id = self.engine.start_workflow("simple-workflow", "wf-unit", {"input": "x"})
        deadline = time.time() + 5
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
        self.assertEqual(status, "COMPLETED")


if __name__ == "__main__":
    unittest.main()
