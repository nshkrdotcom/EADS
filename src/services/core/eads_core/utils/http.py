"""HTTP utility functions."""
from typing import Any, Dict, Optional

import httpx


async def make_request(
    url: str,
    method: str = "GET",
    data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 30,
) -> httpx.Response:
    """Make an HTTP request with error handling.

    Args:
        url: Target URL
        method: HTTP method (GET, POST, etc.)
        data: Request data
        headers: Request headers
        timeout: Request timeout in seconds

    Returns:
        Response object
    """
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=method, url=url, json=data, headers=headers, timeout=timeout
        )
        response.raise_for_status()
        return response
