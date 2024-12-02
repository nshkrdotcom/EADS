"""Error handling module for EADS.

This module provides centralized error handling functionality for the EADS system,
including custom exceptions, error logging, and error response formatting.
"""

import logging
import sys
import traceback
from typing import Any, Dict, Optional

from fastapi import HTTPException, status

from config.settings import LOGGING_CONFIG

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class EADSBaseException(Exception):
    """Base exception class for EADS system."""

    def __init__(self, message: str, error_code: Optional[str] = None) -> None:
        """Initialize the base exception.

        Args:
            message: Error message
            error_code: Optional error code for tracking
        """
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class DatabaseError(EADSBaseException):
    """Exception for database-related errors."""

    pass


class ModelError(EADSBaseException):
    """Exception for ML model-related errors."""

    pass


class ConfigurationError(EADSBaseException):
    """Exception for configuration-related errors."""

    pass


class ValidationError(EADSBaseException):
    """Exception for data validation errors."""

    pass


def handle_exception(
    exc: Exception,
    log_error: bool = True,
    raise_http: bool = True,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
) -> Dict[str, Any]:
    """Handle exceptions in a standardized way.

    Args:
        exc: The exception to handle
        log_error: Whether to log the error
        raise_http: Whether to raise an HTTPException
        status_code: HTTP status code to use if raising HTTPException

    Returns:
        Dict containing error details

    Raises:
        HTTPException: If raise_http is True
    """
    error_type = exc.__class__.__name__
    error_details = {
        "error_type": error_type,
        "message": str(exc),
        "error_code": getattr(exc, "error_code", None),
        "traceback": traceback.format_exc() if log_error else None,
    }

    if log_error:
        logger.error(
            f"Error occurred: {error_type}", extra={"error_details": error_details}
        )

    if raise_http:
        raise HTTPException(status_code=status_code, detail=error_details)

    return error_details


def setup_exception_handlers(app: Any) -> None:
    """Set up FastAPI exception handlers.

    Args:
        app: FastAPI application instance
    """

    @app.exception_handler(EADSBaseException)
    async def eads_exception_handler(request: Any, exc: EADSBaseException):
        """Handle EADS-specific exceptions."""
        return handle_exception(exc)

    @app.exception_handler(DatabaseError)
    async def database_exception_handler(request: Any, exc: DatabaseError):
        """Handle database-related exceptions."""
        return handle_exception(exc, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    @app.exception_handler(ModelError)
    async def model_exception_handler(request: Any, exc: ModelError):
        """Handle ML model-related exceptions."""
        return handle_exception(exc, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Any, exc: ValidationError):
        """Handle validation-related exceptions."""
        return handle_exception(exc, status_code=status.HTTP_400_BAD_REQUEST)


def safe_exit(error: Optional[Exception] = None, exit_code: int = 1) -> None:
    """Safely exit the application with proper cleanup and logging.

    Args:
        error: Optional exception that caused the exit
        exit_code: Exit code to use
    """
    if error:
        logger.error(f"Exiting due to error: {str(error)}")
        logger.debug(traceback.format_exc())
    else:
        logger.info("Application shutting down normally")

    # Perform any necessary cleanup here
    logging.shutdown()
    sys.exit(exit_code)
