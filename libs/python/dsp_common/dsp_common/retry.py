from __future__ import annotations

from typing import Any, Awaitable, Callable, TypeVar

from tenacity import AsyncRetrying, RetryError, Retrying, retry_if_exception, stop_after_attempt, wait_exponential_jitter

T = TypeVar("T")


def retry_sync(
    fn: Callable[[], T],
    *,
    max_attempts: int = 5,
    base: float = 0.1,
    max_wait: float = 5.0,
    is_retryable: Callable[[BaseException], bool] | None = None,
) -> T:
    """
    Retry wrapper with exponential backoff + jitter.
    Use for outbound calls and transient failures only.
    """
    pred = retry_if_exception(is_retryable or (lambda _: True))
    try:
        for attempt in Retrying(
            retry=pred,
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential_jitter(initial=base, max=max_wait),
            reraise=True,
        ):
            with attempt:
                return fn()
    except RetryError as e:  # pragma: no cover
        raise e.last_attempt.exception()  # type: ignore[misc]


async def retry_async(
    fn: Callable[[], Awaitable[T]],
    *,
    max_attempts: int = 5,
    base: float = 0.1,
    max_wait: float = 5.0,
    is_retryable: Callable[[BaseException], bool] | None = None,
) -> T:
    pred = retry_if_exception(is_retryable or (lambda _: True))
    try:
        async for attempt in AsyncRetrying(
            retry=pred,
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential_jitter(initial=base, max=max_wait),
            reraise=True,
        ):
            with attempt:
                return await fn()
    except RetryError as e:  # pragma: no cover
        raise e.last_attempt.exception()  # type: ignore[misc]

