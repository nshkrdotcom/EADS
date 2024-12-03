"""Weaviate client wrapper for EADS."""

from typing import Any, Dict, List, Optional

import weaviate

from .config import WeaviateConfig
from .schema import WeaviateSchema


class WeaviateClient:
    """Client for interacting with Weaviate vector store."""

    def __init__(self, config: WeaviateConfig) -> None:
        """Initialize Weaviate client.

        Args:
            config: WeaviateConfig instance with connection details
        """
        auth_config = (
            weaviate.auth.AuthApiKey(api_key=config.api_key) if config.api_key else None
        )
        self.client: weaviate.Client = weaviate.Client(
            url=config.url, auth_client_secret=auth_config
        )
        self.schema = WeaviateSchema()

    def init_schema(self) -> None:
        """Initialize the schema in Weaviate."""
        # Create CodeSnippet class
        if not self.client.schema.exists("CodeSnippet"):
            self.client.schema.create_class(self.schema.code_schema())

        # Create Pattern class
        if not self.client.schema.exists("Pattern"):
            self.client.schema.create_class(self.schema.pattern_schema())

    def add_code_snippet(
        self, content: str, language: str, tags: List[str], source: str
    ) -> Dict[str, Any]:
        """Add a code snippet to the vector store.

        Args:
            content: The code content
            language: Programming language
            tags: List of tags
            source: Source of the code snippet

        Returns:
            Dict[str, Any]: Response from Weaviate containing the object ID
        """
        result = self.client.data_object.create(
            class_name="CodeSnippet",
            data_object={
                "content": content,
                "language": language,
                "tags": tags,
                "source": source,
            },
        )
        return result  # type: ignore

    def search_similar_code(
        self, query: str, limit: int = 5, filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar code snippets.

        Args:
            query: Search query
            limit: Maximum number of results
            filters: Optional filters to apply

        Returns:
            List[Dict[str, Any]]: List of similar code snippets
        """
        result = (
            self.client.query.get("CodeSnippet")
            .with_near_text({"concepts": [query]})
            .with_limit(limit)
        )

        if filters:
            result = result.with_where(filters)

        response = result.do()
        snippets = response.get("data", {}).get("Get", {}).get("CodeSnippet", [])
        return snippets  # type: ignore

    def add_pattern(
        self, name: str, description: str, template: str, category: str
    ) -> Dict[str, Any]:
        """Add a code pattern to the vector store.

        Args:
            name: Pattern name
            description: Pattern description
            template: Pattern template
            category: Pattern category

        Returns:
            Dict[str, Any]: Response from Weaviate containing the object ID
        """
        result = self.client.data_object.create(
            class_name="Pattern",
            data_object={
                "name": name,
                "description": description,
                "template": template,
                "category": category,
            },
        )
        return result  # type: ignore

    def search_patterns(
        self, query: str, limit: int = 5, category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search for code patterns.

        Args:
            query: Search query
            limit: Maximum number of results
            category: Optional category filter

        Returns:
            List[Dict[str, Any]]: List of matching patterns
        """
        result = (
            self.client.query.get("Pattern")
            .with_near_text({"concepts": [query]})
            .with_limit(limit)
        )

        if category:
            result = result.with_where(
                {"path": ["category"], "operator": "Equal", "valueString": category}
            )

        response = result.do()
        patterns = response.get("data", {}).get("Get", {}).get("Pattern", [])
        return patterns  # type: ignore
