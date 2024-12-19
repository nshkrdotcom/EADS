"""Error handling utilities for EADS."""

from typing import Any, Dict

from fastapi import HTTPException


class ModelError(HTTPException):
    """Custom error for model-related issues."""

    def __init__(self, detail: str) -> None:
        """Initialize ModelError.

        Args:
            detail: Error message
        """
        super().__init__(status_code=400, detail=detail)


def format_error_response(error: Exception) -> Dict[str, Any]:
    """Format error response.

    Args:
        error: Exception to format

    Returns:
        Dict containing error details
    """
    return {
        "error": error.__class__.__name__,
        "message": str(error),
    }
