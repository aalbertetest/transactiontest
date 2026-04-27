"""API keys for machine-to-machine access."""

from __future__ import annotations

import hashlib
import secrets

from sqlalchemy.orm import Session

from payhub.models import ApiKey, User


def generate_api_key() -> tuple[str, str, str]:
    """Return (full_secret, prefix, hash)."""
    secret = "pk_live_" + secrets.token_urlsafe(32)
    prefix = secret[:12]
    digest = hashlib.sha256(secret.encode()).hexdigest()
    return secret, prefix, digest


def verify_api_key(db: Session, secret: str) -> User | None:
    if not secret.startswith("pk_live_"):
        return None
    digest = hashlib.sha256(secret.encode()).hexdigest()
    prefix = secret[:12]
    row = (
        db.query(ApiKey)
        .filter(ApiKey.key_prefix == prefix, ApiKey.key_hash == digest, ApiKey.is_revoked.is_(False))
        .first()
    )
    if not row:
        return None
    return row.user
