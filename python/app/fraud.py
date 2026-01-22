from typing import Dict, Tuple


def evaluate_fraud_signals(payload: Dict[str, object]) -> Tuple[int, str, Dict[str, object]]:
    amount = int(payload["amount"])
    currency = payload.get("currency", "USD")
    signals: Dict[str, object] = {}

    score = 10
    if amount > 50000:
        score += 40
        signals["high_amount"] = True

    if currency not in {"USD", "EUR", "GBP"}:
        score += 20
        signals["unsupported_currency"] = currency

    if payload.get("customer_id") is None:
        score += 10
        signals["guest_checkout"] = True

    decision = "allow"
    if score >= 60:
        decision = "block"
    elif score >= 40:
        decision = "review"

    return score, decision, signals
