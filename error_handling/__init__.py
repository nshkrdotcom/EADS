"""Error handling package for EADS."""

from .error_handler import (
    EADSBaseException,
    DatabaseError,
    ModelError,
    ConfigurationError,
    ValidationError,
    handle_exception,
    setup_exception_handlers,
    safe_exit
)

__all__ = [
    'EADSBaseException',
    'DatabaseError',
    'ModelError',
    'ConfigurationError',
    'ValidationError',
    'handle_exception',
    'setup_exception_handlers',
    'safe_exit'
]
