import time
from typing import Dict

from app.config import (
    BASE_BACKOFF_MS,
    MAX_RETRY_ATTEMPTS,
    WEBHOOK_SIGNING_SECRET,
    WORKER_POLL_INTERVAL_SEC,
)
from app.payments import process_payment_intent
from app.retry import with_retries
from app.storage import STORE
from app.webhooks import deliver_webhook


def handle_process_payment(task: Dict[str, object]) -> None:
    intent_id = str(task["intent_id"])
    intent = STORE.get_payment_intent(intent_id)
    if not intent:
        return
    if intent["status"] != "processing":
        return
    process_payment_intent(STORE, intent)


def handle_deliver_webhooks(task: Dict[str, object]) -> None:
    event_id = str(task["event_id"])
    event = STORE.events.get(event_id)
    if not event:
        return
    endpoints = STORE.list_webhook_endpoints(event["merchant_id"])
    for endpoint in endpoints:
        try:
            with_retries(
                lambda: deliver_webhook(endpoint["url"], WEBHOOK_SIGNING_SECRET, event),
                retryable_exceptions=[Exception],
                max_attempts=MAX_RETRY_ATTEMPTS,
                base_backoff_ms=BASE_BACKOFF_MS,
            )
            STORE.update_event_status(event_id, "delivered")
        except Exception:
            STORE.update_event_status(event_id, "failed")


def run_worker() -> None:
    while True:
        task = STORE.dequeue_task()
        if not task:
            time.sleep(WORKER_POLL_INTERVAL_SEC)
            continue
        task_type = task.get("type")
        if task_type == "process_payment":
            handle_process_payment(task)
        elif task_type == "deliver_webhooks":
            handle_deliver_webhooks(task)


if __name__ == "__main__":
    run_worker()
