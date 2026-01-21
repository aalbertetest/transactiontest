import os


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


DATABASE_URL = os.getenv("DATABASE_URL", "postgres://postgres:postgres@localhost:5432/workflow")
EXECUTOR_ID = os.getenv("EXECUTOR_ID", "executor-1")
POLL_INTERVAL_MS = _get_int("POLL_INTERVAL_MS", 1000)
LOCK_TTL_SECONDS = _get_int("LOCK_TTL_SECONDS", 60)
BATCH_SIZE = _get_int("BATCH_SIZE", 5)
SHARD_COUNT = _get_int("SHARD_COUNT", 16)
SHARDS = os.getenv("SHARDS", "")
METRICS_PORT = _get_int("METRICS_PORT", 8001)
