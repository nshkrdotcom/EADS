"""Test GP service main module."""
from typing import Any, Dict, cast

import pytest
from eads_gp.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    """Create test client."""
    return TestClient(app)


def test_health_check(client: TestClient) -> Dict[Any, Any]:
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    response_data = cast(Dict[Any, Any], response.json())
    assert response_data["status"] == "healthy"
    return response_data
