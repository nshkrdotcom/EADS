"""Core service FastAPI application."""
from typing import Callable

from fastapi import FastAPI, Request, Response
from pydantic import BaseModel

from .config import load_config
from .error_handling import setup_error_handlers
from .logging import ServiceLogger, log_operation
from .tracking import setup_tracking

app = FastAPI(title="EADS Core Service")
logger = ServiceLogger("core")

# Initialize core components
with log_operation("core_initialization") as ctx:
    config = load_config()
    setup_error_handlers(app)
    setup_tracking(app)
    ctx.update(config_loaded=bool(config))
    logger.log_startup(config)


class HealthCheck(BaseModel):
    """Health check response model for the core service.

    Attributes:
        status (str): The current status of the service
        config_loaded (bool): Whether the configuration was loaded successfully
    """

    status: str = "healthy"
    service: str = "core"
    config_loaded: bool = True


@app.middleware("http")
async def log_requests(request: Request, call_next: Callable) -> Response:
    """Log all HTTP requests and responses."""
    ctx = logger.log_request(request.method, request.url.path)
    response = await call_next(request)
    logger.log_response(response.status_code, request_id=ctx.get("request_id"))
    return response


@app.get("/health", response_model=HealthCheck)
async def health_check() -> HealthCheck:
    """Health check endpoint."""
    with log_operation("health_check") as ctx:
        is_loaded = bool(config)
        ctx.update(config_loaded=is_loaded)
        return HealthCheck(config_loaded=is_loaded)
