from __future__ import annotations

import logging
import os
from typing import Any

import structlog


def configure_logging(service_name: str, env: str, level: str) -> None:
    """
    Configure structured JSON logging using structlog.

    Requirements:
    - Never log secrets (tokens/passwords).
    - Add service/env fields to every entry.
    - Prefer explicit correlation fields:
      - request_id
      - trace_id
      - tenant_id
    """

    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, level.upper(), logging.INFO),
    )

    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Bind common fields at root.
    structlog.get_logger().bind(service=service_name, env=env)

    # Best-effort: ensure Python doesn't emit noisy logs by default.
    if os.getenv("DSP_LOG_STD_LIB", "").lower() != "true":
        logging.getLogger("uvicorn").setLevel(logging.WARNING)
        logging.getLogger("asyncio").setLevel(logging.WARNING)


def get_logger(**fields: Any) -> structlog.BoundLogger:
    return structlog.get_logger().bind(**fields)

