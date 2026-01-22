import threading
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional


def generate_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:24]}"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class InMemoryStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.merchants: Dict[str, Dict[str, object]] = {}
        self.payment_intents: Dict[str, Dict[str, object]] = {}
        self.charges: Dict[str, Dict[str, object]] = {}
        self.refunds: Dict[str, Dict[str, object]] = {}
        self.idempotency: Dict[str, Dict[str, object]] = {}
        self.webhook_endpoints: Dict[str, Dict[str, object]] = {}
        self.events: Dict[str, Dict[str, object]] = {}
        self.fraud_assessments: Dict[str, Dict[str, object]] = {}
        self.tasks: List[Dict[str, object]] = []

    def add_merchant(self, name: str, api_key: str) -> Dict[str, object]:
        with self._lock:
            merchant_id = generate_id("mch")
            record = {"id": merchant_id, "name": name, "api_key": api_key}
            self.merchants[merchant_id] = record
            return record

    def get_merchant_by_api_key(self, api_key: str) -> Optional[Dict[str, object]]:
        with self._lock:
            for merchant in self.merchants.values():
                if merchant["api_key"] == api_key:
                    return merchant
        return None

    def get_idempotency(self, merchant_id: str, key: str) -> Optional[Dict[str, object]]:
        return self.idempotency.get(f"{merchant_id}:{key}")

    def set_idempotency(
        self,
        merchant_id: str,
        key: str,
        request_hash: str,
        response_body: Dict[str, object],
        status_code: int,
    ) -> None:
        self.idempotency[f"{merchant_id}:{key}"] = {
            "request_hash": request_hash,
            "response_body": response_body,
            "status_code": status_code,
            "created_at": utc_now(),
        }

    def create_payment_intent(self, merchant_id: str, payload: Dict[str, object]) -> Dict[str, object]:
        with self._lock:
            intent_id = generate_id("pi")
            record = {
                "id": intent_id,
                "merchant_id": merchant_id,
                "amount": payload["amount"],
                "currency": payload["currency"],
                "customer_id": payload.get("customer_id"),
                "payment_method_token": payload["payment_method_token"],
                "capture_method": payload.get("capture_method", "automatic"),
                "metadata": payload.get("metadata", {}),
                "return_url": payload.get("return_url"),
                "status": "requires_confirmation",
                "client_secret": f"{intent_id}_secret_{uuid.uuid4().hex[:16]}",
                "created_at": utc_now(),
                "updated_at": utc_now(),
            }
            self.payment_intents[intent_id] = record
            return record

    def update_payment_intent(self, intent_id: str, updates: Dict[str, object]) -> Dict[str, object]:
        with self._lock:
            record = self.payment_intents[intent_id]
            record.update(updates)
            record["updated_at"] = utc_now()
            return record

    def get_payment_intent(self, intent_id: str) -> Optional[Dict[str, object]]:
        return self.payment_intents.get(intent_id)

    def create_charge(self, intent_id: str, amount: int, currency: str, status: str) -> Dict[str, object]:
        with self._lock:
            charge_id = generate_id("ch")
            record = {
                "id": charge_id,
                "payment_intent_id": intent_id,
                "amount": amount,
                "currency": currency,
                "status": status,
                "created_at": utc_now(),
            }
            self.charges[charge_id] = record
            return record

    def get_charge(self, charge_id: str) -> Optional[Dict[str, object]]:
        return self.charges.get(charge_id)

    def create_refund(self, charge_id: str, amount: int, status: str) -> Dict[str, object]:
        with self._lock:
            refund_id = generate_id("rf")
            record = {
                "id": refund_id,
                "charge_id": charge_id,
                "amount": amount,
                "status": status,
                "created_at": utc_now(),
            }
            self.refunds[refund_id] = record
            return record

    def add_webhook_endpoint(self, merchant_id: str, url: str, enabled: bool) -> Dict[str, object]:
        with self._lock:
            endpoint_id = generate_id("we")
            record = {
                "id": endpoint_id,
                "merchant_id": merchant_id,
                "url": url,
                "enabled": enabled,
                "created_at": utc_now(),
            }
            self.webhook_endpoints[endpoint_id] = record
            return record

    def list_webhook_endpoints(self, merchant_id: str) -> List[Dict[str, object]]:
        return [
            endpoint
            for endpoint in self.webhook_endpoints.values()
            if endpoint["merchant_id"] == merchant_id and endpoint["enabled"]
        ]

    def create_event(self, merchant_id: str, event_type: str, data: Dict[str, object]) -> Dict[str, object]:
        with self._lock:
            event_id = generate_id("evt")
            record = {
                "id": event_id,
                "merchant_id": merchant_id,
                "type": event_type,
                "created_at": utc_now(),
                "data": data,
                "status": "pending",
            }
            self.events[event_id] = record
            self.tasks.append({"type": "deliver_webhooks", "event_id": event_id})
            return record

    def create_fraud_assessment(
        self,
        intent_id: str,
        risk_score: int,
        decision: str,
        signals: Dict[str, object],
    ) -> Dict[str, object]:
        with self._lock:
            assessment_id = generate_id("fra")
            record = {
                "id": assessment_id,
                "payment_intent_id": intent_id,
                "risk_score": risk_score,
                "decision": decision,
                "signals": signals,
                "created_at": utc_now(),
            }
            self.fraud_assessments[assessment_id] = record
            return record

    def list_events(self, merchant_id: str) -> List[Dict[str, object]]:
        return [
            event for event in self.events.values() if event["merchant_id"] == merchant_id
        ]

    def update_event_status(self, event_id: str, status: str) -> None:
        with self._lock:
            if event_id in self.events:
                self.events[event_id]["status"] = status

    def enqueue_task(self, task: Dict[str, object]) -> None:
        with self._lock:
            self.tasks.append(task)

    def dequeue_task(self) -> Optional[Dict[str, object]]:
        with self._lock:
            if not self.tasks:
                return None
            return self.tasks.pop(0)


STORE = InMemoryStore()
