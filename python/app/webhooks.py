import hashlib
import hmac
import json
import time
from typing import Dict

import httpx


def sign_payload(secret: str, payload: Dict[str, object], timestamp: int) -> str:
    message = f"{timestamp}.{json.dumps(payload, separators=(',', ':'))}"
    digest = hmac.new(secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"t={timestamp},v1={digest}"


def deliver_webhook(url: str, secret: str, event: Dict[str, object], timeout: float = 5.0) -> None:
    timestamp = int(time.time())
    signature = sign_payload(secret, event, timestamp)
    headers = {
        "Content-Type": "application/json",
        "Payment-Signature": signature,
    }
    response = httpx.post(url, json=event, headers=headers, timeout=timeout)
    response.raise_for_status()
