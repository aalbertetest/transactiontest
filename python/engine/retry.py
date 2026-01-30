from __future__ import annotations

import math
from typing import Optional

from .models import RetryPolicy


def compute_backoff_seconds(policy: RetryPolicy, attempt: int) -> int:
    """
    Compute exponential backoff with a maximum cap.

    attempt is 1-based (first retry attempt is attempt=1).
    """

    if attempt <= 0:
        return policy.initial_interval_seconds
    interval = policy.initial_interval_seconds * (policy.backoff_coefficient ** (attempt - 1))
    interval = min(interval, policy.max_interval_seconds)
    return int(math.ceil(interval))

