from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    db_path = tmp_path / "test.db"
    return Settings(
        database_url=f"sqlite+aiosqlite:///{db_path}",
        jwt_secret="test-secret",
        instance_id="test-instance",
        delivery_poll_interval=0.05,
        presence_broadcast_interval=0.1,
        delivery_batch_size=10,
        max_retries=3,
        base_retry_seconds=0.0,
        max_retry_seconds=0.1,
        lease_seconds=1.0,
        offline_retry_seconds=0.05,
        enable_background_workers=True,
        enable_presence_broadcast=False,
    )


@pytest.fixture
def app(settings: Settings):
    return create_app(settings)


@pytest.fixture
def client(app):
    with TestClient(app) as client:
        yield client
