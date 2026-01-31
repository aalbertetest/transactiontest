from __future__ import annotations

import base64
import hashlib
import hmac


def issue_token(player_id: str, secret_key: str) -> str:
    digest = hmac.new(
        secret_key.encode("utf-8"),
        player_id.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")


def verify_token(player_id: str, token: str, secret_key: str) -> bool:
    if not token:
        return False
    expected = issue_token(player_id, secret_key)
    return hmac.compare_digest(expected, token)
