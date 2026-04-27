"""Idempotency: stable responses for duplicate POSTs."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from payhub.models import IdempotencyRecord


def _hash(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def idempotency_scope(user_id: str) -> str:
    return f"user:{user_id}"


def build_request_hash(payload: dict) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return _hash(canonical)


def find_record(db: Session, scope: str, idempotency_key: str) -> IdempotencyRecord | None:
    key_h = _hash(idempotency_key)
    return (
        db.query(IdempotencyRecord)
        .filter(IdempotencyRecord.scope == scope, IdempotencyRecord.key_hash == key_h)
        .first()
    )


def save_record(
    db: Session,
    scope: str,
    idempotency_key: str,
    request_hash: str,
    response_status: int,
    response_body: str,
    payment_id: str | None,
) -> None:
    rec = IdempotencyRecord(
        scope=scope,
        key_hash=_hash(idempotency_key),
        request_hash=request_hash,
        response_status=response_status,
        response_body=response_body,
        payment_id=payment_id,
    )
    db.add(rec)


def prune_old(db: Session, ttl_hours: int) -> int:
    cutoff = datetime.utcnow() - timedelta(hours=ttl_hours)
    q = db.query(IdempotencyRecord).filter(IdempotencyRecord.created_at < cutoff)
    count = q.count()
    q.delete(synchronize_session=False)
    return count
