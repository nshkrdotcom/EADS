"""Orchestration package for EADS workflows using Dagster."""

from dagster import Definitions

from .assets.core_assets import core_assets
from .assets.llm_assets import gemini_response, gemini_service
from .jobs.core_jobs import core_job

defs = Definitions(
    assets=[*core_assets, gemini_service, gemini_response],
    jobs=[core_job],
)
