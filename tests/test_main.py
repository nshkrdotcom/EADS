"""Test module for EADS main functionality."""
import pytest
from fastapi.testclient import TestClient
from neo4j import AsyncDriver
from pytest_asyncio import fixture

from src.gp_engine.gp_service import app as gp_app
from src.init.knowledge_base_init import initialize_knowledge_base
from src.nlp.nlp_service import app as nlp_app


@fixture(scope="function")
def gp_client() -> TestClient:
    """Create a test client for the GP service.

    Returns:
        TestClient: FastAPI test client for GP service
    """
    return TestClient(gp_app)


@fixture(scope="function")
def nlp_client() -> TestClient:
    """Create a test client for the NLP service.

    Returns:
        TestClient: FastAPI test client for NLP service
    """
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
    assert "best_individual" in result
    assert "fitness" in result


def test_nlp_encode(nlp_client: TestClient) -> None:
    """Test NLP encode endpoint."""
    input_data = {"text": "Example code"}
    response = nlp_client.post("/encode", json=input_data)
    assert response.status_code == 200
    result = response.json()
    assert "encoding" in result


def test_nlp_analyze(nlp_client: TestClient) -> None:
    """Test NLP analyze endpoint."""
    input_data = {"code": "def example(): pass"}
    response = nlp_client.post("/analyze", json=input_data)
    assert response.status_code == 200
    result = response.json()
    assert "patterns" in result


@pytest.mark.asyncio
async def test_end_to_end_flow(
    neo4j_driver: AsyncDriver,
    gp_client: TestClient,
    nlp_client: TestClient,
) -> None:
    """Test end-to-end flow including database initialization and service calls.

    Args:
        neo4j_driver: Neo4j async driver instance
        gp_client: FastAPI test client for GP service
        nlp_client: FastAPI test client for NLP service
    """
    # Initialize knowledge base
    await initialize_knowledge_base(neo4j_driver)

    # Test NLP service
    nlp_response = nlp_client.post("/encode", json={"text": "Example code"})
    assert nlp_response.status_code == 200
    encoding = nlp_response.json()["encoding"]

    # Test GP service with encoded input
    gp_response = gp_client.post(
        "/evolve",
        json={
            "code": "def example(): pass",
            "population_size": 10,
            "generations": 5,
            "mutation_rate": 0.1,
            "crossover_rate": 0.7,
            "encoding": encoding,
        },
    )
    assert gp_response.status_code == 200
    assert "best_individual" in gp_response.json()
