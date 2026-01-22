from typing import Dict, Optional

from .config import BASE_BACKOFF_MS, MAX_RETRY_ATTEMPTS
from .fraud import evaluate_fraud_signals
from .processor import ProcessorClient, ProcessorDeclinedError, RetryableProcessorError
from .retry import with_retries
from .storage import InMemoryStore


def process_payment_intent(store: InMemoryStore, intent: Dict[str, object]) -> Optional[Dict[str, object]]:
    risk_score, decision, signals = evaluate_fraud_signals(intent)
    store.create_fraud_assessment(intent["id"], risk_score, decision, signals)

    if decision == "block":
        store.update_payment_intent(intent["id"], {"status": "failed"})
        store.create_event(
            intent["merchant_id"],
            "payment_intent.failed",
            {"id": intent["id"], "status": "failed", "reason": "fraud_block"},
        )
        return None

    processor = ProcessorClient()

    def attempt() -> str:
        return processor.authorize(
            int(intent["amount"]), str(intent["currency"]), str(intent["payment_method_token"])
        )

    try:
        processor_reference = with_retries(
            attempt,
            retryable_exceptions=[RetryableProcessorError],
            max_attempts=MAX_RETRY_ATTEMPTS,
            base_backoff_ms=BASE_BACKOFF_MS,
        )
        charge = store.create_charge(
            intent["id"], int(intent["amount"]), str(intent["currency"]), "succeeded"
        )
        store.update_payment_intent(
            intent["id"],
            {"status": "succeeded", "charge_id": charge["id"], "processor_reference": processor_reference},
        )
        store.create_event(
            intent["merchant_id"],
            "payment_intent.succeeded",
            {"id": intent["id"], "status": "succeeded", "charge_id": charge["id"]},
        )
        return charge
    except ProcessorDeclinedError:
        store.update_payment_intent(intent["id"], {"status": "failed"})
        store.create_event(
            intent["merchant_id"],
            "payment_intent.failed",
            {"id": intent["id"], "status": "failed", "reason": "declined"},
        )
    except RetryableProcessorError:
        store.update_payment_intent(intent["id"], {"status": "failed"})
        store.create_event(
            intent["merchant_id"],
            "payment_intent.failed",
            {"id": intent["id"], "status": "failed", "reason": "processor_unavailable"},
        )
    return None
