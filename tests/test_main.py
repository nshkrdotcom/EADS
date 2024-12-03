"""Test module for EADS main functionality."""

from typing import AsyncGenerator

from fastapi.testclient import TestClient
from neo4j import AsyncGraphDatabase, Driver
from pytest import fixture

from EADS.config.settings import NEO4J_PASSWORD, NEO4J_URI, NEO4J_USER
from EADS.gp_engine.gp_service import app as gp_app
from EADS.init.knowledge_base_init import initialize_knowledge_base
from EADS.nlp.nlp_service import app as nlp_app


@fixture(scope="module")  # type: ignore[misc]
async def neo4j_driver() -> AsyncGenerator[Driver, None]:
    """Create a Neo4j driver for testing.

    Yields:
        Driver: Neo4j driver instance
    """
    driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    initialize_knowledge_base(driver)  # Initialize without storing result
    yield driver
    await driver.close()


@fixture(scope="module", name="gp_client")  # type: ignore[misc]
def gp_client_fixture() -> TestClient:
    """Create a test client for the GP service.

    Returns:
        TestClient: FastAPI test client
    """
    return TestClient(gp_app)


@fixture(scope="module", name="nlp_client")  # type: ignore[misc]
def nlp_client_fixture() -> TestClient:
    """Create a test client for the NLP service.

    Returns:
        TestClient: FastAPI test client
    """
    return TestClient(nlp_app)


def test_gp_service_root(gp_client_fixture: TestClient) -> None:
    """Test GP service root endpoint.

    Args:
        gp_client_fixture: GP service test client
    """
    response = gp_client_fixture.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "GP Service is running"}


def test_nlp_service_root(nlp_client_fixture: TestClient) -> None:
    """Test NLP service root endpoint.

    Args:
        nlp_client_fixture: NLP service test client
    """
    response = nlp_client_fixture.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "NLP Service is running"}


def test_gp_evolve(gp_client_fixture: TestClient) -> None:
    """Test GP evolve endpoint.

    Args:
        gp_client_fixture: GP service test client
    """
    input_data = {
        "code": "def example(): pass",
        "population_size": 10,
        "generations": 5,
        "mutation_rate": 0.1,
        "crossover_rate": 0.7,
    }
    response = gp_client_fixture.post("/evolve", json=input_data)
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "success"
    assert "solution" in result
    assert "fitness" in result["solution"]
    assert "individual" in result["solution"]
    assert "generation" in result["solution"]


def test_nlp_encode(nlp_client_fixture: TestClient) -> None:
    """Test NLP encode endpoint.

    Args:
        nlp_client_fixture: NLP service test client
    """
    response = nlp_client_fixture.post("/encode", json={"text": "def example(): pass"})
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "success"
    assert "encoding" in result
    assert isinstance(result["encoding"], list)


def test_nlp_analyze(nlp_client_fixture: TestClient) -> None:
    """Test NLP analyze endpoint.

    Args:
        nlp_client_fixture: NLP service test client
    """
    response = nlp_client_fixture.post("/analyze", json={"code": "def example(): pass"})
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "success"
    assert "patterns" in result
    assert isinstance(result["patterns"], list)


def test_end_to_end_flow(
    neo4j_driver: Driver,
    gp_client_fixture: TestClient,
    nlp_client_fixture: TestClient,
) -> None:
    """Test end-to-end flow.

    Args:
        neo4j_driver: Neo4j driver fixture
        gp_client_fixture: GP service test client
        nlp_client_fixture: NLP service test client
    """
    # Initialize knowledge base
    init_result = initialize_knowledge_base(neo4j_driver)
    assert init_result["status"] == "success"

    # Test code analysis
    code = "def example(): pass"
    nlp_response = nlp_client_fixture.post("/analyze", json={"code": code})
    assert nlp_response.status_code == 200
    nlp_result = nlp_response.json()
    assert nlp_result["status"] == "success"

    # Test code evolution
    gp_response = gp_client_fixture.post(
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
