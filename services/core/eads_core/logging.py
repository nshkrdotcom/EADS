"""Core logging configuration and utilities."""
import os
from contextlib import contextmanager
from time import perf_counter
from typing import Optional, Any, Dict, Callable
import traceback

import structlog

VALID_LOG_LEVELS = {"debug", "info", "warning", "error"}
DEFAULT_LOG_LEVEL = "info"

def add_global_context(_, __, event_dict):
    """Add global context to all log entries."""
    event_dict.update({
        "environment": os.getenv("ENVIRONMENT", "development"),
        "version": os.getenv("VERSION", "dev"),
    })
    return event_dict

def configure_logging(service_name: str):
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

def get_logger():
    """Get a structured logger instance."""
    return structlog.get_logger()

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
        >>> with log_operation("process_request", request_id=123) as ctx:
        ...     result = process(request)
        ...     ctx.update(result_size=len(result))
        ...     return result
    """
    if level not in VALID_LOG_LEVELS:
        level = DEFAULT_LOG_LEVEL
        logger = get_logger()
        logger.warning(f"Invalid log level '{level}' provided. Using default level: {DEFAULT_LOG_LEVEL}")

    context = dict(initial_context)
    start = perf_counter() if include_timing else None
    logger = get_logger()
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

class ServiceLogger:
    """Service-specific logger with common logging patterns."""
    
    def __init__(self, service_name: str):
        """Initialize service logger.
        
        Args:
            service_name: Name of the service
        """
        configure_logging(service_name)
        self.logger = get_logger()
    
    def log_startup(self, config: Dict[str, Any]):
        """Log service startup with configuration."""
        with log_operation("service_startup") as ctx:
            ctx.update(config={k: v for k, v in config.items() if not k.endswith("_key")})
    
    def log_shutdown(self):
        """Log service shutdown."""
        with log_operation("service_shutdown"):
            pass
    
    def log_request(self, method: str, path: str, **kwargs):
        """Log HTTP request."""
        with log_operation("http_request", 
                         method=method,
                         path=path,
                         level="debug",
                         **kwargs) as ctx:
            return ctx
    
    def log_response(self, status_code: int, **kwargs):
        """Log HTTP response."""
        with log_operation("http_response",
                         status_code=status_code,
                         level="debug",
                         **kwargs) as ctx:
            return ctx
