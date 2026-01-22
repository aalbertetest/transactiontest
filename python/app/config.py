import os


def get_env(name: str, default: str) -> str:
    value = os.getenv(name)
    return value if value is not None else default


ENV = get_env("APP_ENV", "development")
API_KEY = get_env("API_KEY", "test_key_123")
WEBHOOK_SIGNING_SECRET = get_env("WEBHOOK_SIGNING_SECRET", "whsec_test_123")
MAX_RETRY_ATTEMPTS = int(get_env("MAX_RETRY_ATTEMPTS", "5"))
BASE_BACKOFF_MS = int(get_env("BASE_BACKOFF_MS", "200"))
WORKER_POLL_INTERVAL_SEC = float(get_env("WORKER_POLL_INTERVAL_SEC", "0.5"))
