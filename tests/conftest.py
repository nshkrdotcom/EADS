"""Test configuration and fixtures."""
from pathlib import Path
from typing import AsyncGenerator

from neo4j import AsyncDriver, AsyncGraphDatabase
from pytest_asyncio import fixture

from src.config.settings import NEO4J_PASSWORD, NEO4J_URI, NEO4J_USER

# Add project root to PYTHONPATH
root_dir = Path(__file__).parent.parent
src_dir = root_dir / "src"

for path in [str(root_dir), str(src_dir)]:
    if path not in __import__("sys").path:
        __import__("sys").path.insert(0, path)


@fixture(scope="function")
async def neo4j_driver() -> AsyncGenerator[AsyncDriver, None]:
    """Create a Neo4j driver instance for testing.

    Yields:
        AsyncDriver: Neo4j async driver instance
    """
    driver = AsyncGraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASSWORD),
    )
    await driver.verify_connectivity()
    yield driver
    await driver.close()
