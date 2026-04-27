"""Payment orchestration (atomicity, fraud, idempotency)."""

from __future__ import annotations

import json

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from payhub.fraud import evaluate_payment, should_block
from payhub.idempotency import (
    build_request_hash,
    find_record,
    idempotency_scope,
    save_record,
)
from payhub.ledger import compute_fee, journal_balances, post_p2p_payment
from payhub.models import PaymentTransaction, User


class IdempotencyConflictError(Exception):
    """Same idempotency key, different body."""

    pass


class FraudBlockedError(Exception):
    def __init__(self, flags: list[str]) -> None:
        self.flags = flags
        super().__init__("fraud_blocked")


def create_payment(
    db: Session,
    payer: User,
    payee_user_id: str,
    amount_cents: int,
    idempotency_key: str | None,
) -> tuple[PaymentTransaction, bool]:
    """Returns (payment, from_cache). from_cache True if replayed idempotency."""
    payload = {
        "payee_user_id": payee_user_id,
        "amount_cents": amount_cents,
    }
    req_hash = build_request_hash(payload)

    scope: str | None = None
    if idempotency_key:
        scope = idempotency_scope(payer.id)
        existing = find_record(db, scope, idempotency_key)
        if existing:
            if existing.request_hash != req_hash:
                raise IdempotencyConflictError()
            pay = db.get(PaymentTransaction, existing.payment_id) if existing.payment_id else None
            if pay:
                return pay, True
            raise IdempotencyConflictError()

    payee = db.get(User, payee_user_id)
    if not payee:
        raise ValueError("payee_not_found")

    fraud = evaluate_payment(db, payer, payee, amount_cents)
    flags_str = ",".join(fraud.flags) if fraud.flags else None
    if should_block(fraud):
        if idempotency_key and scope:
            save_record(
                db,
                scope,
                idempotency_key,
                req_hash,
                403,
                json.dumps({"detail": "fraud_blocked", "flags": fraud.flags}),
                None,
            )
            db.commit()
        raise FraudBlockedError(fraud.flags)

    fee = compute_fee(amount_cents)

    try:
        payment = post_p2p_payment(
            db,
            payer,
            payee,
            amount_cents,
            fee,
            idempotency_key,
            flags_str,
        )
        deb, cred = journal_balances(db, payment.id)
        if deb != cred:
            raise RuntimeError("ledger_unbalanced")
        if idempotency_key:
            save_record(
                db,
                idempotency_scope(payer.id),
                idempotency_key,
                req_hash,
                201,
                json.dumps({"payment_id": payment.id}),
                payment.id,
            )
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise

    return payment, False
