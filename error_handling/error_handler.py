"""Error handling module for EADS."""

from typing import Any, Dict, Optional, Union

from fastapi import Request, status
from fastapi.responses import JSONResponse


class EADSBaseException(Exception):
    """Base exception class for EADS."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: Optional[str] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            status_code: HTTP status code
            error_code: Internal error code
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or "EADS_ERROR"


class DatabaseError(EADSBaseException):
    """Exception for database-related errors."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_503_SERVICE_UNAVAILABLE,
        error_code: str = "DB_ERROR",
    ) -> None:
        """Initialize database error.

        Args:
            message: Error message
            status_code: HTTP status code
            error_code: Internal error code
        """
        super().__init__(message, status_code, error_code)


class ModelError(EADSBaseException):
    """Exception for model-related errors."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = "MODEL_ERROR",
    ) -> None:
        """Initialize model error.

        Args:
            message: Error message
            status_code: HTTP status code
            error_code: Internal error code
        """
        super().__init__(message, status_code, error_code)


class ValidationError(EADSBaseException):
    """Exception for validation errors."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: str = "VALIDATION_ERROR",
    ) -> None:
        """Initialize validation error.

        Args:
            message: Error message
            status_code: HTTP status code
            error_code: Internal error code
        """
        super().__init__(message, status_code, error_code)


def handle_exception(
    exc: Union[EADSBaseException, Exception],
) -> Dict[str, Any]:
    """Handle exceptions and return appropriate response.

    Args:
        exc: Exception to handle

    Returns:
        Dictionary with error details
    """
    if isinstance(exc, EADSBaseException):
        return {
            "status": "error",
            "message": exc.message,
            "error_code": exc.error_code,
            "status_code": exc.status_code,
        }

    return {
        "status": "error",
        "message": str(exc),
        "error_code": "UNKNOWN_ERROR",
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
    }


async def eads_exception_handler(
    request: Request,
    exc: EADSBaseException,
) -> JSONResponse:
    """Handle FastAPI exceptions for EADS.

    Args:
        request: FastAPI request
        exc: EADS exception

    Returns:
        JSON response with error details
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.message,
            "error_code": exc.error_code,
        },
    )


def register_exception_handlers(app: Any) -> None:
    """Register exception handlers with FastAPI app.

    Args:
        app: FastAPI application instance
    """
    app.add_exception_handler(EADSBaseException, eads_exception_handler)

    for exc_class in [DatabaseError, ModelError, ValidationError]:
        app.add_exception_handler(exc_class, eads_exception_handler)
