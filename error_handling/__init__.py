"""Error handling package."""

from error_handling.error_handler import (
    DatabaseError,
    EADSBaseException,
    ModelError,
    ValidationError,
    eads_exception_handler,
    handle_exception,
    register_exception_handlers,
)

__all__ = [
    "DatabaseError",
    "EADSBaseException",
    "ModelError",
    "ValidationError",
    "eads_exception_handler",
    "handle_exception",
    "register_exception_handlers",
]
