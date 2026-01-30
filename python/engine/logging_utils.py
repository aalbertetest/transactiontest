from __future__ import annotations

import logging
import sys
from typing import Optional


def configure_logging(level: str = "INFO") -> None:
    """
    Configure logging with a consistent format.
    """

    logger = logging.getLogger()
    logger.setLevel(level.upper())
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )
    handler.setFormatter(formatter)
    logger.handlers = [handler]


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

