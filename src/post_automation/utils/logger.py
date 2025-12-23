"""Logging configuration."""

import logging
import sys
from typing import Optional

from post_automation.utils.config import get_settings


def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Set up and configure a logger.

    Args:
        name: Logger name. If None, uses root logger.

    Returns:
        Configured logger instance.
    """
    settings = get_settings()
    logger = logging.getLogger(name)

    # Set log level
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger.setLevel(log_level)

    # Remove existing handlers
    logger.handlers.clear()

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    # Create formatter
    if settings.log_format == "json":
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
            '"logger": "%(name)s", "message": "%(message)s"}'
        )
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


# Default application logger
app_logger = setup_logger("post_automation")
