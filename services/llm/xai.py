r"""xAI (Grok) API integration.

This module provides a clean interface to the xAI Grok API, supporting both
text and vision capabilities.

Example Usage:

1. Basic text generation:
```python
api = GrokAPI(api_key="your-key-here")
response = await api.acall("What is the meaning of life?")
```

2. Vision capabilities:
```python
# Configure for vision
api = GrokAPI(
    api_key="your-key-here",
    model=GrokModel.VISION
)

# Single image
response = await api.acall(
    prompt="What's in this image?",
    images=[ImageContent(
        url="https://example.com/image.jpg",
        detail="high"
    )]
)

# Multiple images
response = await api.acall(
    prompt="Compare these diagrams",
    images=[
        ImageContent(url="https://example.com/diagram1.jpg"),
        ImageContent(url="https://example.com/diagram2.jpg")
    ]
)
```

3. System messages and streaming:
```python
api = GrokAPI(
    api_key="your-key-here",
    stream=True
)

async for chunk in api.astream(
    prompt="Hello!",
    system_message="You are a friendly assistant"
):
    print(chunk, end="", flush=True)
```
"""

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, AsyncGenerator, Dict, List, Optional

import httpx


class GrokModel(str, Enum):
    """Available Grok model types."""

    TEXT = "grok-1-base"
    VISION = "grok-1-vision"


@dataclass
class ImageContent:
    """Image content for vision capabilities."""

    url: str
    detail: str = "high"

    def to_dict(self) -> Dict[str, str]:
        """Convert to API-compatible dict."""
        return {"url": self.url, "detail": self.detail}


class APIError(Exception):
    """Raised when the API returns an error."""

    pass


class ConfigurationError(Exception):
    """Raised when there's an issue with the API configuration."""

    pass


class GrokAPI:
    """Interface to the xAI Grok API."""

    def __init__(
        self,
        api_key: str,
        api_base: str = "https://api.x.ai/v1",
        model: str = GrokModel.TEXT,
        temperature: float = 0,
        stream: bool = False,
    ) -> None:
        """Initialize the Grok API interface.

        Args:
            api_key: xAI API key
            api_base: Base URL for API
            model: Model to use (from GrokModel enum)
            temperature: Sampling temperature
            stream: Whether to stream responses
        """
        if not api_key:
            raise ConfigurationError("API key is required")

        self.api_key = api_key
        self.api_base = api_base.rstrip("/")
        self.model = model
        self.temperature = temperature
        self.stream = stream

    def _prepare_messages(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        images: Optional[List[ImageContent]] = None,
    ) -> List[Dict[str, Any]]:
        """Prepare messages for API request.

        Args:
            prompt: Input prompt
            system_message: Optional system message
            images: Optional list of images

        Returns:
            List[Dict[str, Any]]: Formatted messages

        Raises:
            ConfigurationError: If images are provided for non-vision model
        """
        if images and self.model != GrokModel.VISION:
            raise ConfigurationError(
                f"Images provided but model {self.model} doesn't support vision"
            )

        messages: List[Dict[str, Any]] = []
        if system_message:
            messages.append({"role": "system", "content": system_message})

        # Build user message content
        content: List[Dict[str, Any]] = [{"type": "text", "text": prompt}]
        if images:
            content.extend(
                [{"type": "image", "image": img.to_dict()} for img in images]
            )

        # Add user message with content array
        messages.append({"role": "user", "content": content})
        return messages

    async def _acall(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        images: Optional[List[ImageContent]] = None,
        stop: Optional[List[str]] = None,
    ) -> str:
        """Make an async call to the Grok API.

        Args:
            prompt: Input prompt
            system_message: Optional system message
            images: Optional list of images (for vision model)
            stop: Optional list of stop sequences

        Returns:
            str: Generated response

        Raises:
            APIError: If the API returns an error
            ConfigurationError: If there's an issue with the configuration
            ValueError: If prompt is empty
        """
        if not prompt:
            raise ValueError("Prompt is required")

        messages = self._prepare_messages(prompt, system_message, images)
        data = {
            "messages": messages,
            "model": self.model,
            "temperature": self.temperature,
            "stream": self.stream,
        }
        if stop:
            data["stop"] = stop

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_base}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=30.0,
                )

                if response.status_code != 200:
                    error = response.json().get("error", {})
                    message = error.get("message", "Unknown error")
                    raise APIError(f"API error: {message}")

                result = response.json()
                return str(result["choices"][0]["message"]["content"])

        except httpx.TimeoutException as e:
            raise APIError(f"API request timed out: {str(e)}")
        except httpx.RequestError as e:
            raise APIError(f"API request failed: {str(e)}")
        except (KeyError, json.JSONDecodeError) as e:
            raise APIError(f"Invalid API response: {str(e)}")

    async def astream(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        images: Optional[List[ImageContent]] = None,
        stop: Optional[List[str]] = None,
    ) -> AsyncGenerator[str, None]:
        """Stream responses from the Grok API.

        Args:
            prompt: Input prompt
            system_message: Optional system message
            images: Optional list of images (for vision model)
            stop: Optional list of stop sequences

        Yields:
            str: Generated response chunks

        Raises:
            APIError: If the API returns an error
            ConfigurationError: If there's an issue with the configuration
        """
        if not self.stream:
            raise ConfigurationError("Streaming is not enabled")

        # Save current stream setting
        original_stream = self.stream
        try:
            # Force stream=True for this call
            self.stream = True
            response = await self._acall(
                prompt=prompt, system_message=system_message, images=images, stop=stop
            )
            # For now, just yield the full response
            # TODO: Implement proper streaming when API supports it
            yield str(response)
        finally:
            # Restore original stream setting
            self.stream = original_stream
