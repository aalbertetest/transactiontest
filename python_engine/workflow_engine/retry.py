"""
Retry and backoff helpers.
"""

from __future__ import annotations

import random

from .models import RetryPolicy


def compute_backoff_seconds(attempt: int, policy: RetryPolicy) -> float:
    if attempt <= 0:
        return policy.initial_interval_seconds
    interval = policy.initial_interval_seconds * (policy.backoff_coefficient ** (attempt - 1))
    interval = min(interval, policy.max_interval_seconds)
    jitter = interval * 0.1
    return interval + random.uniform(-jitter, jitter)


def should_retry(attempt: int, policy: RetryPolicy) -> bool:
    return attempt < policy.max_attempts
