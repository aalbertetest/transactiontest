"""
Exponential backoff with jitter.
"""

from __future__ import annotations

import random


def compute_backoff_seconds(
    attempt: int,
    initial_seconds: float,
    max_seconds: float,
    jitter: float,
) -> float:
    """
    Compute exponential backoff with jitter in seconds.

    attempt is 1-based (first retry attempt).
    """
    exp = min(max_seconds, initial_seconds * (2 ** max(0, attempt - 1)))
    if jitter <= 0:
        return exp
    # Apply jitter as +/- percentage.
    delta = exp * jitter
    return max(0.0, exp + random.uniform(-delta, delta))
