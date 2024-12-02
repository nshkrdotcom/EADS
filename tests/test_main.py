"""Test cases for main functionality."""

import os
from unittest.mock import MagicMock, patch

import pytest

from gp_engine.gp_service import GPService
from init.db_init import KnowledgeBaseInitializer
from nlp.nlp_service import NLPService


@pytest.fixture
def mock_neo4j_driver():
    """Fixture for mocking Neo4j driver."""
    with patch("neo4j.GraphDatabase") as mock_driver:
        mock_session = MagicMock()
        mock_driver.driver.return_value.session.return_value = mock_session
        yield mock_driver


@pytest.fixture
def knowledge_base_init():
    """Fixture for KnowledgeBaseInitializer instance."""
    return KnowledgeBaseInitializer()


@pytest.fixture
def gp_service():
    """Fixture for GPService instance."""
    return GPService(population_size=50)


@pytest.fixture
def nlp_service():
    """Fixture for NLPService instance."""
    return NLPService()


def test_knowledge_base_initialization(mock_neo4j_driver, knowledge_base_init):
    """Test knowledge base initialization."""
    # Test successful initialization
    assert knowledge_base_init.init_knowledge_base() is True

    # Verify constraint creation
    mock_session = mock_neo4j_driver.driver.return_value.session.return_value
    mock_session.run.assert_called()


def test_gp_service_evolution(gp_service):
    """Test genetic programming evolution process."""
    # Test with valid parameters
    fitness_history = gp_service.evolve(generations=5)
    assert isinstance(fitness_history, dict)
    assert "best_fitness" in fitness_history

    # Test with invalid parameters
    with pytest.raises(ValueError):
        gp_service.evolve(generations=0)


def test_nlp_service_processing(nlp_service):
    """Test NLP service text processing."""
    test_text = "Test design pattern implementation"
    result = nlp_service.process_text(test_text)
    assert isinstance(result, dict)
    assert "processed_text" in result


@pytest.mark.integration
def test_end_to_end_flow():
    """Integration test for end-to-end flow."""
    # Skip if running in CI environment
    if os.getenv("CI"):
        pytest.skip("Skipping integration test in CI environment")

    # Initialize components
    kb_init = KnowledgeBaseInitializer()
    gp_service = GPService()
    nlp_service = NLPService()

    # Test complete flow
    assert kb_init.init_knowledge_base()
    assert isinstance(gp_service.evolve(generations=1), dict)
    assert isinstance(nlp_service.process_text("Test pattern"), dict)
