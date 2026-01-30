import os
import time

from engine import (
    Config,
    DBTaskQueue,
    MetricsRegistry,
    SQLiteStore,
    TimerScheduler,
    WorkflowEngine,
    Worker,
    configure_logging,
)


def greeting_workflow(ctx, input_payload):
    # Versioning API ensures backward compatibility across workflow code changes.
    version = yield ctx.get_version("greeting-change", 1, 2)
    name = input_payload.get("name", "world")
    greeting = yield ctx.execute_activity(
        "compose_greeting",
        {"name": name},
        schedule_to_close_timeout_seconds=30,
        start_to_close_timeout_seconds=10,
        heartbeat_timeout_seconds=5,
    )
    yield ctx.sleep(1)
    approval = yield ctx.wait_signal("approval")
    return {
        "greeting": greeting,
        "approved_by": approval.get("user"),
        "version": version,
    }


def compose_greeting(activity_ctx, input_payload):
    activity_ctx.heartbeat({"stage": "starting"})
    return f"Hello, {input_payload['name']}!"


def run_example():
    configure_logging("INFO")
    if os.path.exists("example.db"):
        os.remove("example.db")
    config = Config(db_path="example.db", task_queue_name="default", worker_id="python-worker")
    metrics = MetricsRegistry()
    store = SQLiteStore(config.db_path)
    queue = DBTaskQueue(store.connection, metrics=metrics)
    engine = WorkflowEngine(store, queue, config, metrics=metrics)
    worker = Worker(store, queue, config, metrics=metrics)
    worker.register_workflow("GreetingWorkflow", greeting_workflow)
    worker.register_activity("compose_greeting", compose_greeting)
    scheduler = TimerScheduler(store, queue, config, metrics=metrics)

    scheduler.start()
    worker.start()

    run_id = engine.start_workflow(
        workflow_id="greeting-workflow-1",
        workflow_type="GreetingWorkflow",
        input_payload={"name": "Temporal"},
    )

    time.sleep(2)
    engine.signal_workflow(
        workflow_id="greeting-workflow-1",
        run_id=run_id,
        signal_name="approval",
        payload={"user": "admin@example.com"},
    )

    while True:
        execution = store.get_workflow_execution("greeting-workflow-1", run_id)
        if execution and execution["state"] == "COMPLETED":
            print("Workflow result:", execution["result"])
            break
        time.sleep(0.5)

    worker.stop()
    scheduler.stop()
    print("Metrics:", metrics.snapshot())


if __name__ == "__main__":
    run_example()

