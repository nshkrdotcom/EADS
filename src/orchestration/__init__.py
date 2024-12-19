"""Orchestration package for EADS workflows using Dagster."""

from dagster import Definitions

from utils.env import load_env
from utils.logger import setup_logger

from .assets.core_assets import core_assets
from .assets.llm_assets import gemini_response, gemini_service
from .assets.xai_assets import grok_response, grok_service
from .jobs.core_jobs import core_job

# Set up logger
logger = setup_logger("eads.orchestration")

# Load and validate environment
validation = load_env()
if not validation.is_valid:
    logger.error("Environment configuration is invalid")
    # We don't raise an error here because some assets might not need all variables
    # Individual assets will fail if they can't get their required variables

defs = Definitions(
    assets=[*core_assets, gemini_service, gemini_response, grok_service, grok_response],
    jobs=[core_job],
)
