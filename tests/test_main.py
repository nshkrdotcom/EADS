"""Test module for EADS main functionality."""
import pytest
from httpx import ASGITransport, AsyncClient
from neo4j import AsyncDriver
from pytest_asyncio import fixture

from src.gp_engine.gp_service import app as gp_app
from src.init.knowledge_base_init import initialize_knowledge_base
from src.nlp.nlp_service import app as nlp_app


@fixture(scope="function")
async def gp_client() -> AsyncClient:
    """Create a test client for the GP service.

    Returns:
        AsyncClient: HTTPX async client for GP service
    """
    async with AsyncClient(
        transport=ASGITransport(app=gp_app), base_url="http://test"
    ) as client:
        yield client


@fixture(scope="function")
async def nlp_client() -> AsyncClient:
    """Create a test client for the NLP service.

    Returns:
        AsyncClient: HTTPX async client for NLP service
    """
    async with AsyncClient(
        transport=ASGITransport(app=nlp_app), base_url="http://test"
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_gp_service_root(gp_client: AsyncClient) -> None:
    """Test GP service root endpoint."""
    response = await gp_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "GP Service is running"}


@pytest.mark.asyncio
async def test_nlp_service_root(nlp_client: AsyncClient) -> None:
    """Test NLP service root endpoint."""
    response = await nlp_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "NLP Service is running"}


@pytest.mark.asyncio
async def test_gp_evolve(gp_client: AsyncClient) -> None:
    """Test GP evolve endpoint."""
    input_data = {
        "code": "def example(): pass",
        "population_size": 10,
        "generations": 5,
        "mutation_rate": 0.1,
        "crossover_rate": 0.7,
    }
    response = await gp_client.post("/evolve", json=input_data)
    assert response.status_code == 200
    result = response.json()
    assert "best_individual" in result
    assert isinstance(result["best_individual"], str)


@pytest.mark.asyncio
async def test_nlp_encode(nlp_client: AsyncClient) -> None:
    """Test NLP encode endpoint."""
    input_data = {"text": "Example code"}
    response = await nlp_client.post("/encode", json=input_data)
    assert response.status_code == 200
    result = response.json()
    assert "encoding" in result


@pytest.mark.asyncio
async def test_nlp_analyze(nlp_client: AsyncClient) -> None:
    """Test NLP analyze endpoint."""
    input_data = {"code": "def example(): pass"}
    response = await nlp_client.post("/analyze", json=input_data)
    assert response.status_code == 200
    result = response.json()
    assert "patterns" in result


@pytest.mark.asyncio
async def test_end_to_end_flow(
    neo4j_driver: AsyncDriver,
    gp_client: AsyncClient,
    nlp_client: AsyncClient,
) -> None:
    """Test end-to-end flow including database initialization and service calls.

    Args:
        neo4j_driver: Neo4j async driver instance
        gp_client: HTTPX async client for GP service
        nlp_client: HTTPX async client for NLP service
    """
    # Initialize knowledge base
    await initialize_knowledge_base(neo4j_driver)

    # Test NLP service
    nlp_response = await nlp_client.post("/encode", json={"text": "Example code"})
    assert nlp_response.status_code == 200
    assert "encoding" in nlp_response.json()

    # Test GP service
    gp_response = await gp_client.post(
        "/evolve",
        json={
            "code": "def example(): pass",
            "population_size": 10,
            "generations": 5,
            "mutation_rate": 0.1,
            "crossover_rate": 0.7,
        },
    )
    assert gp_response.status_code == 200
    assert "best_individual" in gp_response.json()
