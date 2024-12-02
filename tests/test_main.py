"""Test module for EADS main functionality."""

import pytest
from fastapi.testclient import TestClient
from neo4j import AsyncGraphDatabase, Driver

from gp_engine.gp_service import app as gp_app
from init.knowledge_base_init import init_knowledge_base
from nlp.nlp_service import app as nlp_app


@pytest.fixture(scope="module")
def neo4j_driver() -> Driver:
    """Create a Neo4j driver for testing.

    Returns:
        Driver: Neo4j driver instance
    """
    driver = AsyncGraphDatabase.driver(
        "bolt://localhost:7687", auth=("neo4j", "password")
    )
    init_knowledge_base(driver)
    return driver


@pytest.fixture(scope="module")
def gp_client() -> TestClient:
    """Create a test client for the GP service.

    Returns:
        TestClient: FastAPI test client
    """
    return TestClient(gp_app)


@pytest.fixture(scope="module")
def nlp_client() -> TestClient:
    """Create a test client for the NLP service.

    Returns:
        TestClient: FastAPI test client
    """
    return TestClient(nlp_app)


def test_gp_service_root(gp_client: TestClient) -> None:
    """Test GP service root endpoint.

    Args:
        gp_client: GP service test client
    """
    response = gp_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "GP Service is running"}


def test_nlp_service_root(nlp_client: TestClient) -> None:
    """Test NLP service root endpoint.

    Args:
        nlp_client: NLP service test client
    """
    response = nlp_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "NLP Service is running"}


def test_gp_evolve(gp_client: TestClient) -> None:
    """Test GP evolve endpoint.

    Args:
        gp_client: GP service test client
    """
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
    """Test NLP encode endpoint.

    Args:
        nlp_client: NLP service test client
    """
    response = nlp_client.post("/encode", json={"text": "def example(): pass"})
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "success"
    assert "encoding" in result
    assert isinstance(result["encoding"], list)


def test_nlp_analyze(nlp_client: TestClient) -> None:
    """Test NLP analyze endpoint.

    Args:
        nlp_client: NLP service test client
    """
    response = nlp_client.post("/analyze", json={"code": "def example(): pass"})
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "success"
    assert "patterns" in result
    assert isinstance(result["patterns"], list)


def test_end_to_end_flow(
    neo4j_driver: Driver,
    gp_client: TestClient,
    nlp_client: TestClient,
) -> None:
    """Test end-to-end flow.

    Args:
        neo4j_driver: Neo4j driver fixture
        gp_client: GP service test client
        nlp_client: NLP service test client
    """
    # Initialize knowledge base
    init_result = init_knowledge_base(neo4j_driver)
    assert init_result["status"] == "success"

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
