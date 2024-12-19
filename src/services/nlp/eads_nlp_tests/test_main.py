"""Test NLP service main module."""
from typing import Any, Dict, cast
from unittest.mock import Mock, patch

import pytest
from eads_nlp.logging import log_operation
from fastapi.testclient import TestClient

# Create a mock Weaviate client that returns True for is_ready
mock_client = Mock()
mock_client.is_ready.return_value = True

# Mock WeaviateClient before importing app
with patch("eads_nlp.vector_store.client.weaviate.Client", return_value=mock_client):
    from eads_nlp.main import app


@pytest.fixture
def client() -> TestClient:
    """Create test client."""
    return TestClient(app)


def test_health_check(client: TestClient) -> Dict[Any, Any]:
    """Test health check endpoint."""
    with log_operation("health_check") as ctx:
        response = client.get("/health")
        ctx.update(status_code=response.status_code)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.json()}")
        assert response.status_code == 200
        response_data = cast(Dict[Any, Any], response.json())
        assert response_data["status"] == "healthy"
        assert response_data["vector_store_ready"] is True
        return response_data
