"""Schema definitions for Weaviate classes."""

from typing import Dict


class WeaviateSchema:
    """Schema manager for Weaviate classes."""

    @staticmethod
    def code_schema() -> Dict[str, object]:
        """Define schema for code snippets."""
        return {
            "class": "CodeSnippet",
            "description": "A code snippet with associated metadata",
            "properties": [
                {
                    "name": "content",
                    "dataType": ["text"],
                    "description": "The actual code content",
                },
                {
                    "name": "language",
                    "dataType": ["text"],
                    "description": "Programming language",
                },
                {
                    "name": "tags",
                    "dataType": ["text[]"],
                    "description": "Associated tags",
                },
                {
                    "name": "source",
                    "dataType": ["text"],
                    "description": "Source of the code snippet",
                },
            ],
            "vectorIndexConfig": {"distance": "cosine"},
        }

    @staticmethod
    def pattern_schema() -> Dict[str, object]:
        """Define schema for code patterns."""
        return {
            "class": "Pattern",
            "description": "A code pattern or template",
            "properties": [
                {"name": "name", "dataType": ["text"], "description": "Pattern name"},
                {
                    "name": "description",
                    "dataType": ["text"],
                    "description": "Pattern description",
                },
                {
                    "name": "template",
                    "dataType": ["text"],
                    "description": "Pattern template",
                },
                {
                    "name": "category",
                    "dataType": ["text"],
                    "description": "Pattern category",
                },
            ],
            "vectorIndexConfig": {"distance": "cosine"},
        }
