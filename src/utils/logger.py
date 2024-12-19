"""Logging configuration for EADS."""

import logging
import sys
from pathlib import Path
from typing import Optional

# Configure logging format
LOGGER_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup_logger(
    name: str, level: int = logging.INFO, log_file: Optional[Path] = None
) -> logging.Logger:
    """Set up a logger with consistent formatting.

    Args:
        name: Logger name
        level: Logging level
        log_file: Optional path to log file

    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(LOGGER_FORMAT)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
