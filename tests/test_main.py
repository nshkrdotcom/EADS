"""Test module for EADS main functionality."""

import pytest
from fastapi.testclient import TestClient
from neo4j import AsyncDriver

from src.gp_engine.gp_service import app as gp_app
from src.init.knowledge_base_init import initialize_knowledge_base
from src.nlp.nlp_service import app as nlp_app


@pytest.fixture
def gp_client() -> TestClient:
    """Create a test client for the GP service."""
    return TestClient(gp_app)


@pytest.fixture
def nlp_client() -> TestClient:
    """Create a test client for the NLP service."""
    return TestClient(nlp_app)


def test_gp_service_root(gp_client: TestClient) -> None:
    """Test GP service root endpoint."""
    response = gp_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "GP Service is running"}


def test_nlp_service_root(nlp_client: TestClient) -> None:
    """Test NLP service root endpoint."""
    response = nlp_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "NLP Service is running"}


def test_gp_evolve(gp_client: TestClient) -> None:
    """Test GP evolve endpoint."""
    input_data = {
        "code": "def example(): pass",
        "population_size": 10,
        "generations": 5,
        "mutation_rate": 0.1,
        "crossover_rate": 0.7,
    }
    response = gp_client.post("/evolve", json=input_data)
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "success"
    assert "solution" in result
    assert "fitness" in result["solution"]
    assert "individual" in result["solution"]
    assert "generation" in result["solution"]


def test_nlp_encode(nlp_client: TestClient) -> None:
    """Test NLP encode endpoint."""
    response = nlp_client.post("/encode", json={"text": "def example(): pass"})
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "success"
    assert "encoding" in result
    assert isinstance(result["encoding"], list)


def test_nlp_analyze(nlp_client: TestClient) -> None:
    """Test NLP analyze endpoint."""
    response = nlp_client.post("/analyze", json={"code": "def example(): pass"})
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "success"
    assert "patterns" in result
    assert isinstance(result["patterns"], list)


@pytest.mark.asyncio
async def test_end_to_end_flow(
    neo4j_driver: AsyncDriver,
    gp_client: TestClient,
    nlp_client: TestClient,
) -> None:
    """Test end-to-end flow."""
    # Initialize knowledge base
    result = await initialize_knowledge_base(neo4j_driver)
    assert result["status"] == "success"

    # Test code analysis
    code = "def example(): pass"
    nlp_response = nlp_client.post("/analyze", json={"code": code})
    assert nlp_response.status_code == 200
    nlp_result = nlp_response.json()
    assert nlp_result["status"] == "success"

    # Test code evolution
    gp_response = gp_client.post(
        "/evolve",
        json={
            "code": code,
            "population_size": 10,
            "generations": 5,
            "mutation_rate": 0.1,
            "crossover_rate": 0.7,
        },
    )
    assert gp_response.status_code == 200
    gp_result = gp_response.json()
    assert gp_result["status"] == "success"
