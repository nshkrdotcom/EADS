"""xAI-related Dagster assets.

Example Usage:

1. Basic text generation:
```python
# Through Dagster ops
result = await grok_response(
    prompt="What is the meaning of life?",
    temperature=0.7,
    system_message="You are a philosopher"
)
```

2. Image analysis:
```python
# Configure for vision model
config = XAIConfig(model=GrokModel.VISION)

# Create service
vision_service = grok_service(config)

# Analyze image
result = await grok_response(
    grok_service=vision_service,
    prompt="What's in this image?",
    images=[{
        "url": "https://example.com/image.jpg",
        "detail": "high"
    }]
)

# Compare multiple images
result = await grok_response(
    grok_service=vision_service,
    prompt="Compare these diagrams",
    images=[
        {"url": "https://example.com/diagram1.jpg"},
        {"url": "https://example.com/diagram2.jpg"}
    ],
    system_message="You are an expert at analyzing technical diagrams"
)
```

3. Configuration options:
```python
# Custom configuration
config = XAIConfig(
    api_key="your-key-here",
    model=GrokModel.TEXT,
    temperature=0.7,
    stream=True
)

# Create service with custom config
custom_service = grok_service(config)

# Use service
result = await grok_response(
    grok_service=custom_service,
    prompt="Hello!",
    system_message="Be friendly"
)
```
"""

import os
from typing import Dict, List, Optional

from dagster import AssetExecutionContext, Config, asset

from services.llm.xai import GrokAPI, GrokModel, ImageContent


class XAIConfig(Config):
    """Configuration for xAI assets."""

    api_key: str = os.getenv("XAI_API_KEY", "")
    api_base: str = "https://api.x.ai/v1"
    model: str = GrokModel.TEXT
    temperature: float = 0
    stream: bool = False


@asset
def grok_service(config: XAIConfig) -> GrokAPI:
    """Create a configured instance of the Grok API service.

    Args:
        config: Configuration for the Grok service

    Returns:
        GrokAPI: Configured Grok API instance
    """
    return GrokAPI(
        api_key=config.api_key,
        api_base=config.api_base,
        model=config.model,
        temperature=config.temperature,
        stream=config.stream,
    )


@asset
async def grok_response(
    context: AssetExecutionContext,
    grok_service: GrokAPI,
    prompt: str,
    system_message: Optional[str] = None,
    images: Optional[List[Dict[str, str]]] = None,
    stop: Optional[List[str]] = None,
    temperature: Optional[float] = None,
    stream: Optional[bool] = None,
) -> str:
    """Generate a response using the Grok model.

    Args:
        context: Dagster execution context
        grok_service: Configured Grok service
        prompt: Input prompt for the model
        system_message: Optional system message
        images: Optional list of image URLs with detail level
               Example: [{"url": "http://...", "detail": "high"}]
        stop: Optional list of stop sequences
        temperature: Optional temperature override
        stream: Optional stream override

    Returns:
        str: Generated response from Grok
    """
    if temperature is not None:
        grok_service.temperature = temperature
    if stream is not None:
        grok_service.stream = stream

    # Convert image dicts to ImageContent objects
    image_contents = None
    if images:
        image_contents = [
            ImageContent(url=img["url"], detail=img.get("detail", "high"))
            for img in images
        ]

    try:
        response = await grok_service._acall(
            prompt=prompt,
            system_message=system_message,
            images=image_contents,
            stop=stop,
        )
        context.log.info(f"Generated response: {response}")
        return str(response)

    except Exception as e:
        context.log.error(f"Error generating response: {str(e)}")
        raise
