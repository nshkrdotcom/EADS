"""NLP service logging configuration."""
from eads_core.logging import (
    ServiceLogger,
    configure_logging,
    get_logger,
    log_operation,
)

# Configure NLP service logging
configure_logging("nlp")
logger = get_logger()

__all__ = ["ServiceLogger", "log_operation", "logger"]
