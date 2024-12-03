"""Weaviate client wrapper for EADS."""

from typing import Any, Dict, List, Optional

import weaviate

from ..logging import log_operation
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
        with log_operation("init_weaviate_schema") as ctx:
            # Create CodeSnippet class
            code_exists = self.client.schema.exists("CodeSnippet")
            if not code_exists:
                self.client.schema.create_class(self.schema.code_schema())

            # Create Pattern class
            pattern_exists = self.client.schema.exists("Pattern")
            if not pattern_exists:
                self.client.schema.create_class(self.schema.pattern_schema())

            ctx.update(code_exists=code_exists, pattern_exists=pattern_exists)

    def is_ready(self) -> bool:
        """Check if Weaviate is ready.

        Returns:
            bool: True if Weaviate is ready, False otherwise
        """
        with log_operation("check_weaviate_ready") as ctx:
            try:
                is_ready = bool(self.client.is_ready())
                ctx.update(is_ready=is_ready)
                return is_ready
            except Exception as e:
                ctx.update(error=str(e))
                return False

    def add_code_snippet(
        self, content: str, language: str, tags: List[str], source: str
    ) -> Dict[str, Any]:
        """Add a code snippet to the vector store."""
        with log_operation(
            "add_code_snippet",
            content_length=len(content),
            language=language,
            num_tags=len(tags),
            source=source,
        ) as ctx:
            result = self.client.data_object.create(
                class_name="CodeSnippet",
                data_object={
                    "content": content,
                    "language": language,
                    "tags": tags,
                    "source": source,
                },
            )
            ctx.update(object_id=result.get("id"))
            return result

    def search_similar_code(
        self, query: str, limit: int = 5, filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar code snippets."""
        with log_operation(
            "search_similar_code",
            query_length=len(query),
            limit=limit,
            has_filters=filters is not None,
        ) as ctx:
            result = (
                self.client.query.get("CodeSnippet")
                .with_near_text({"concepts": [query]})
                .with_limit(limit)
            )

            if filters:
                result = result.with_where(filters)

            response = result.do()
            snippets = response.get("data", {}).get("Get", {}).get("CodeSnippet", [])
            ctx.update(num_results=len(snippets))
            return snippets

    def add_pattern(
        self, name: str, description: str, template: str, category: str
    ) -> Dict[str, Any]:
        """Add a pattern to the vector store."""
        with log_operation(
            "add_pattern",
            name=name,
            description_length=len(description),
            template_length=len(template),
            category=category,
        ) as ctx:
            result = self.client.data_object.create(
                class_name="Pattern",
                data_object={
                    "name": name,
                    "description": description,
                    "template": template,
                    "category": category,
                },
            )
            ctx.update(object_id=result.get("id"))
            return result

    def search_patterns(
        self, query: str, limit: int = 5, category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search for code patterns."""
        with log_operation(
            "search_patterns",
            query_length=len(query),
            limit=limit,
            has_category=category is not None,
        ) as ctx:
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
            ctx.update(num_results=len(patterns))
            return patterns
