import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


@pytest.fixture()
def client(tmp_path):
    settings = Settings(
        database_url=f"sqlite+aiosqlite:///{tmp_path / 'test.db'}",
        redis_url=None,
        secret_key="test-secret",
        matchmaking_size=2,
        max_input_rate=20,
        max_speed=6.0,
        state_ttl_seconds=60,
    )
    app = create_app(settings)
    with TestClient(app) as test_client:
        yield test_client
