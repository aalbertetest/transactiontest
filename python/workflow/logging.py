"""
Logging helpers for the workflow engine.
"""

from __future__ import annotations

import logging
from typing import Optional


def configure_logging(level: str = "INFO") -> None:
    """
    Configure a consistent logging format for the engine.
    """
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Retrieve a logger with the standard engine naming.
    """
    return logging.getLogger(name or "workflow")
