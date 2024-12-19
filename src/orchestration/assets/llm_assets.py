"""LLM-related Dagster assets."""

import os
from typing import Optional

from dagster import AssetExecutionContext, Config, asset

from services.llm.gemini import GeminiService


class GeminiConfig(Config):
    """Configuration for Gemini assets."""

    api_key: str = os.getenv("GOOGLE_API_KEY", "")
    model_name: str = "gemini-pro"


@asset
def gemini_service(config: GeminiConfig) -> GeminiService:
    """Create a configured instance of the Gemini service.

    Args:
        config: Configuration for the Gemini service

    Returns:
        GeminiService: Configured Gemini service instance
    """
    return GeminiService(api_key=config.api_key, model_name=config.model_name)


@asset
async def gemini_response(
    context: AssetExecutionContext,
    gemini_service: GeminiService,
    prompt: str,
    system_message: Optional[str] = None,
) -> str:
    """Generate a response using the Gemini model.

    Args:
        context: Dagster execution context
        gemini_service: Configured Gemini service
        prompt: Input prompt for the model
        system_message: Optional system message for context

    Returns:
        str: Generated response from Gemini
    """
    response: str = await gemini_service.generate_response(
        prompt=prompt, system_message=system_message
    )

    context.log.info(f"Generated response: {response}")
    return response
