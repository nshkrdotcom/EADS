"""Request tracking middleware for EADS."""
import uuid

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from ..logging import get_logger

logger = get_logger()


class RequestTrackingMiddleware(BaseHTTPMiddleware):
    """Middleware for tracking HTTP requests.

    Adds a unique request ID to each request and tracks request/response metrics.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Process the request and add tracking information.

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response: FastAPI response
        """
        request_id = str(uuid.uuid4())
        logger.debug(
            "request_started",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )

        response = await call_next(request)

        logger.debug(
            "request_completed",
            request_id=request_id,
            status_code=response.status_code,
        )
        response.headers["X-Request-ID"] = request_id
        return response


def setup_tracking(app: FastAPI) -> None:
    """Set up request tracking for FastAPI application.

    Args:
        app: FastAPI application instance
    """
    app.add_middleware(RequestTrackingMiddleware)
