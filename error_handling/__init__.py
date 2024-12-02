"""Error handling package for EADS."""

from .error_handler import (
    ConfigurationError,
    DatabaseError,
    EADSBaseException,
    ModelError,
    ValidationError,
    handle_exception,
    safe_exit,
    setup_exception_handlers,
)

__all__ = [
    "EADSBaseException",
    "DatabaseError",
    "ModelError",
    "ConfigurationError",
    "ValidationError",
    "handle_exception",
    "setup_exception_handlers",
    "safe_exit",
]
