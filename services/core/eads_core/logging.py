"""Core logging configuration and utilities for EADS services."""
import os
import traceback
from contextlib import contextmanager
from time import perf_counter
from typing import Any, Callable, Dict, Generator, Optional, TypeVar

import structlog

VALID_LOG_LEVELS = {"debug", "info", "warning", "error"}
DEFAULT_LOG_LEVEL = "info"

T = TypeVar("T")
LogContext = Dict[str, Any]
ErrorHandler = Callable[[Exception, str, LogContext], None]


def add_global_context(
    logger: structlog.types.BindableLogger,
    method_name: str,
    event_dict: Dict[str, Any],
) -> Dict[str, Any]:
    """Add global context to all log entries.

    Args:
        logger: The logger instance
        method_name: Name of the logging method
        event_dict: Current event dictionary

    Returns:
        Dict[str, Any]: Updated event dictionary with global context
    """
    event_dict.update(
        {
            "environment": os.getenv("ENVIRONMENT", "development"),
            "version": os.getenv("VERSION", "dev"),
        }
    )
    return event_dict


def configure_logging(service_name: str) -> None:
    """Configure structured logging for a service.

    Args:
        service_name: Name of the service (e.g., 'core', 'nlp', 'gp')
    """
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            add_global_context,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Set service name in context
    structlog.contextvars.bind_contextvars(service=service_name)


def get_logger() -> structlog.BoundLogger:
    """Get a structured logger instance.

    Returns:
        structlog.BoundLogger: Configured logger instance
    """
    return structlog.get_logger()


@contextmanager
def log_operation(
    operation: str,
    level: str = DEFAULT_LOG_LEVEL,
    include_timing: bool = True,
    error_handler: Optional[ErrorHandler] = None,
    **initial_context: Any,
) -> Generator[LogContext, None, None]:
    """Log an operation with timing and error tracking.

    Args:
        operation: Name of operation being performed
        level: Log level (debug, info, warning, error)
        include_timing: Whether to track operation timing
        error_handler: Optional custom error handler function
        **initial_context: Initial context values to log

    Yields:
        LogContext: Mutable context dictionary that can be updated during
            operation.

    Example:
        >>> with log_operation("process_request", request_id=123) as ctx:
        ...     result = process(request)
        ...     ctx.update(result_size=len(result))
        ...     return result
    """
    if level not in VALID_LOG_LEVELS:
        level = DEFAULT_LOG_LEVEL
        logger = get_logger()
        msg = (
            f"Invalid log level '{level}' provided. "
            f"Using default level: {DEFAULT_LOG_LEVEL}"
        )
        logger.warning(msg)

    context: LogContext = dict(initial_context)
    start: Optional[float] = perf_counter() if include_timing else None
    logger = get_logger()
    log = getattr(logger, level)

    try:
        log(f"{operation}_started", **context)
        yield context

        if include_timing and start is not None:
            context["elapsed_seconds"] = perf_counter() - start
        log(f"{operation}_completed", **context)

    except Exception as e:
        if include_timing and start is not None:
            context["elapsed_seconds"] = perf_counter() - start

        if error_handler:
            error_handler(e, operation, context)
        else:
            logger.error(
                f"{operation}_failed",
                error=str(e),
                error_type=type(e).__name__,
                traceback=traceback.format_exc(),
                **context,
            )
        raise


class ServiceLogger:
    """Service-specific logger with common logging patterns."""

    def __init__(self, service_name: str) -> None:
        """Initialize service logger.

        Args:
            service_name: Name of the service
        """
        configure_logging(service_name)
        self.logger = get_logger()

    def log_startup(self, config: Dict[str, Any]) -> LogContext:
        """Log service startup with configuration.

        Args:
            config: Service configuration dictionary

        Returns:
            LogContext: Context with startup information
        """
        with log_operation("service_startup") as ctx:
            ctx.update(
                config={k: v for k, v in config.items() if not k.endswith("_key")}
            )
            return ctx

    def log_shutdown(self) -> None:
        """Log service shutdown."""
        with log_operation("service_shutdown"):
            pass

    def log_request(self, method: str, path: str, **kwargs: Any) -> LogContext:
        """Log HTTP request.

        Args:
            method: HTTP method
            path: Request path
            **kwargs: Additional context

        Returns:
            LogContext: Request context
        """
        with log_operation(
            operation="http_request", method=method, path=path, level="debug", **kwargs
        ) as ctx:
            return ctx

    def log_response(self, status_code: int, **kwargs: Any) -> LogContext:
        """Log HTTP response.

        Args:
            status_code: HTTP status code
            **kwargs: Additional context

        Returns:
            LogContext: Response context
        """
        with log_operation(
            operation="http_response", status_code=status_code, level="debug", **kwargs
        ) as ctx:
            return ctx
