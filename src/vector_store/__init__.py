"""Vector store module for EADS."""

from .client import WeaviateClient
from .config import WeaviateConfig
from .schema import WeaviateSchema

__all__ = ["WeaviateClient", "WeaviateConfig", "WeaviateSchema"]
