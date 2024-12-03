"""Test configuration and fixtures."""
import os
import sys
import pytest
from pytest_asyncio import fixture
from neo4j import AsyncGraphDatabase, AsyncDriver
from pathlib import Path

from src.config.settings import NEO4J_PASSWORD, NEO4J_URI, NEO4J_USER

# Add both project root and src to PYTHONPATH
root_dir = Path(__file__).parent.parent
src_dir = root_dir / "src"

# Ensure both paths are in sys.path
for path in [str(root_dir), str(src_dir)]:
    if path not in sys.path:
        sys.path.insert(0, path)


@fixture(scope="function")
async def neo4j_driver() -> AsyncDriver:
    """Create a Neo4j driver instance for testing."""
    driver = AsyncGraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASSWORD)
    )
    await driver.verify_connectivity()
    return driver  # Return the driver directly
