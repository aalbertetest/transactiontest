"""Rules-based fraud scoring (deterministic for tests)."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from payhub.models import PaymentTransaction, User


@dataclass
class FraudResult:
    score: int  # 0 = clean, higher = riskier
    flags: list[str]


def evaluate_payment(
    db: Session,
    payer: User,
    payee: User,
    amount_cents: int,
) -> FraudResult:
    flags: list[str] = []
    score = 0

    if payer.id == payee.id:
        flags.append("self_payment")
        score += 50

    if amount_cents >= 1_000_000_00:  # $1M
        flags.append("high_amount")
        score += 30

    recent = (
        db.query(PaymentTransaction)
        .filter(PaymentTransaction.payer_user_id == payer.id)
        .order_by(PaymentTransaction.created_at.desc())
        .limit(10)
        .all()
    )
    if len(recent) >= 8:
        flags.append("velocity_spike")
        score += 25

    if not payee.is_active:
        flags.append("inactive_payee")
        score += 40

    return FraudResult(score=score, flags=flags)


def should_block(result: FraudResult, threshold: int = 45) -> bool:
    return result.score >= threshold
