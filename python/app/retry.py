import random
import time
from typing import Callable, Iterable, Type, TypeVar

T = TypeVar("T")


def with_retries(
    operation: Callable[[], T],
    retryable_exceptions: Iterable[Type[BaseException]],
    max_attempts: int,
    base_backoff_ms: int,
) -> T:
    for attempt in range(1, max_attempts + 1):
        try:
            return operation()
        except tuple(retryable_exceptions):
            if attempt == max_attempts:
                raise
            sleep_ms = base_backoff_ms * (2 ** (attempt - 1))
            jitter = random.randint(0, int(base_backoff_ms * 0.2))
            time.sleep((sleep_ms + jitter) / 1000.0)
    raise RuntimeError("retry attempts exhausted")
