from __future__ import annotations

import structlog
from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from payhub.db import get_db
from payhub.deps import require_user
from payhub.idempotency import find_record, idempotency_scope
from payhub.models import LedgerEntry, PaymentTransaction, User
from payhub.payments_service import FraudBlockedError, IdempotencyConflictError, create_payment
from payhub.rate_limit import limiter
from payhub.schemas import LedgerLineOut, PaymentCreate, PaymentOut

router = APIRouter(prefix="/v1/payments", tags=["payments"])
log = structlog.get_logger("payments")


def _payment_out(db: Session, p: PaymentTransaction) -> PaymentOut:
    lines = db.query(LedgerEntry).filter(LedgerEntry.payment_id == p.id).all()
    ledger = [
        LedgerLineOut(account_id=le.account_id, side=le.side, amount_cents=le.amount_cents)
        for le in lines
    ]
    return PaymentOut(
        id=p.id,
        payer_user_id=p.payer_user_id,
        payee_user_id=p.payee_user_id,
        amount_cents=p.amount_cents,
        fee_cents=p.fee_cents,
        status=p.status,
        fraud_flags=p.fraud_flags,
        created_at=p.created_at,
        ledger=ledger,
    )


@router.post("", response_model=PaymentOut, status_code=status.HTTP_201_CREATED)
@limiter.limit("30/minute")
def create_payment_endpoint(
    request: Request,
    body: PaymentCreate,
    response: Response,
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> PaymentOut:
    key = idempotency_key or body.idempotency_key
    log.info("payment_request", payer=user.id, payee=body.payee_user_id, amount=body.amount_cents)
    try:
        payment, cached = create_payment(
            db,
            user,
            body.payee_user_id,
            body.amount_cents,
            key,
        )
    except IdempotencyConflictError:
        raise HTTPException(status_code=409, detail="idempotency_key_conflict")
    except FraudBlockedError as e:
        raise HTTPException(status_code=403, detail={"code": "fraud_blocked", "flags": e.flags})
    except ValueError as e:
        if str(e) == "payee_not_found":
            raise HTTPException(status_code=404, detail="payee_not_found")
        raise
    if cached:
        response.status_code = status.HTTP_200_OK
        if key:
            rec = find_record(db, idempotency_scope(user.id), key)
            if rec:
                response.headers["X-Idempotency-Replayed"] = "true"
    return _payment_out(db, payment)


@router.get("/{payment_id}", response_model=PaymentOut)
def get_payment(
    payment_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
) -> PaymentOut:
    p = db.get(PaymentTransaction, payment_id)
    if not p:
        raise HTTPException(status_code=404, detail="not_found")
    if p.payer_user_id != user.id and p.payee_user_id != user.id:
        raise HTTPException(status_code=403, detail="forbidden")
    return _payment_out(db, p)
