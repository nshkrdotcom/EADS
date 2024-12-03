"""Core service FastAPI application."""
from fastapi import FastAPI
from pydantic import BaseModel

from core.config import load_config
from core.error_handling import setup_error_handlers
from core.tracking import setup_tracking

app = FastAPI(title="EADS Core Service")

# Initialize core components
config = load_config()
setup_error_handlers(app)
setup_tracking(app)


class HealthCheck(BaseModel):
    """Health check response model for the core service.

    Attributes:
        status (str): The current status of the service
        config_loaded (bool): Whether the configuration was loaded successfully
    """

    status: str = "healthy"
    service: str = "core"
    config_loaded: bool = True


@app.get("/health", response_model=HealthCheck)
async def health_check() -> HealthCheck:
    """Health check endpoint."""
    return HealthCheck(config_loaded=bool(config))
