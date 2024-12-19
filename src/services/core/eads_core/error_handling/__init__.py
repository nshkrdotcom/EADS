"""Error handling module for EADS."""
from fastapi import FastAPI


def setup_error_handlers(app: FastAPI) -> None:
    """Set up FastAPI error handlers.

    Args:
        app: FastAPI application instance
    """
    from starlette.exceptions import HTTPException as StarletteHTTPException

    from .handlers import general_exception_handler, http_exception_handler

    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)


__all__ = ["setup_error_handlers"]
