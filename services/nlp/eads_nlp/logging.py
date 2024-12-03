import structlog
from contextlib import contextmanager
from time import perf_counter
from typing import Optional, Any, Dict, Callable
import traceback

VALID_LOG_LEVELS = {"debug", "info", "warning", "error"}
DEFAULT_LOG_LEVEL = "info"

def add_global_context(_, __, event_dict):
    """Add global context to all log entries."""
    event_dict["service"] = "nlp"
    event_dict["environment"] = "development"  # TODO: Make configurable
    return event_dict

# Configure structlog
structlog.configure(
    processors=[
        add_global_context,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

@contextmanager
def log_operation(
    operation: str,
    level: str = DEFAULT_LOG_LEVEL,
    include_timing: bool = True,
    error_handler: Optional[Callable[[Exception, str, Dict[str, Any]], None]] = None,
    **initial_context: Any
) -> Dict[str, Any]:
    """Log an operation with timing and error tracking.

    Args:
        operation: Name of operation being performed.
        level: Log level (debug, info, warning, error). Defaults to "info".
        include_timing: Whether to track operation timing (default: True).
        error_handler: Optional custom error handler function.
        **initial_context: Initial context values to log.

    Yields:
        Dict[str, Any]: Mutable context dictionary that can be updated during operation.

    Example:
        >>> with log_operation("process_text", text_length=len(text)) as ctx:
        ...     result = process_text(text)
        ...     ctx.update(tokens=len(result["tokens"]))
        ...     return result
    """
    if level not in VALID_LOG_LEVELS:
        level = DEFAULT_LOG_LEVEL
        logger.warning(f"Invalid log level '{level}' provided. Using default level: {DEFAULT_LOG_LEVEL}")

    context = dict(initial_context)
    start = perf_counter() if include_timing else None
    log = getattr(logger, level)

    try:
        log(f"{operation}_started", **context)
        yield context

        if include_timing:
            context["elapsed_seconds"] = perf_counter() - start
        log(f"{operation}_completed", **context)

    except Exception as e:
        if include_timing:
            context["elapsed_seconds"] = perf_counter() - start
        if error_handler:
            error_handler(e, operation, context)
        else:
            logger.error(
                f"{operation}_failed",
                error=str(e),
                error_type=type(e).__name__,
                traceback=traceback.format_exc(),
                **context
            )
        raise
