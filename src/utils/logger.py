"""Logging configuration for EADS with structured logging support."""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union

import structlog
from pythonjsonlogger import jsonlogger

# Configure logging format for traditional logging
LOGGER_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configure structured logging processors
processors = [
    structlog.contextvars.merge_contextvars,
    structlog.processors.add_log_level,
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.JSONRenderer(serializer=json.dumps),
]


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter with additional fields."""

    def add_fields(
        self,
        log_record: Dict[str, Any],
        record: logging.LogRecord,
        message_dict: Dict[str, Any],
    ) -> None:
        """Add custom fields to the log record.

        Args:
            log_record: The log record to add fields to
            record: The logging record
            message_dict: Additional message dictionary
        """
        super().add_fields(log_record, record, message_dict)
        log_record["timestamp"] = datetime.utcnow().isoformat()
        log_record["level"] = record.levelname
        log_record["logger"] = record.name


def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    structured: bool = True,
) -> logging.Logger:
    """Set up a logger with consistent formatting and structured logging support.

    Args:
        name: Logger name
        level: Logging level
        log_file: Optional path to log file
        structured: Whether to use structured logging (JSON format)

    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers = []  # Clear any existing handlers

    if structured:
        # JSON formatter for structured logging
        formatter: Union[CustomJsonFormatter, logging.Formatter] = CustomJsonFormatter(
            "%(timestamp)s %(level)s %(name)s %(message)s"
        )
    else:
        # Traditional formatter
        formatter = logging.Formatter(LOGGER_FORMAT)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler if specified
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(str(log_file))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_structured_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger with proper configuration.

    Args:
        name: Logger name

    Returns:
        structlog.BoundLogger: Configured structured logger
    """
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.BoundLogger,
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger(name)


# Example usage:
# Regular logger:
# logger = setup_logger("my_service", structured=True)
# logger.info("Starting service", extra={"version": "1.0.0"})

# Structured logger:
# logger = get_structured_logger("my_service")
# logger.info("starting_service", version="1.0.0", env="development")
