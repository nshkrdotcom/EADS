"""Configuration for Weaviate vector store."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class WeaviateConfig:
    """Configuration for Weaviate client."""

    host: str
    port: int
    scheme: str = "http"
    api_key: Optional[str] = None

    @property
    def url(self) -> str:
        """Get the full URL for Weaviate connection."""
        return f"{self.scheme}://{self.host}:{self.port}"
