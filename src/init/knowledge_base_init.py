"""Knowledge base initialization module."""

import logging
from typing import Dict, Any

from neo4j import AsyncDriver

logger = logging.getLogger(__name__)


async def initialize_knowledge_base(driver: AsyncDriver) -> Dict[str, Any]:
    """Initialize the knowledge base with required constraints and indexes.

    Args:
        driver: Neo4j driver instance

    Returns:
        Dict[str, Any]: Status of initialization
    """
    try:
        session = await driver.session()
        try:
            # Create constraints and indexes in a single transaction
            query = """
            CREATE CONSTRAINT unique_code_pattern IF NOT EXISTS
            FOR (p:Pattern) REQUIRE p.code IS UNIQUE;
            CREATE INDEX pattern_code_index IF NOT EXISTS
            FOR (p:Pattern) ON (p.code)
            """
            await session.run(query)
            logger.info("Knowledge base initialized successfully")
            return {"status": "success", "message": "Knowledge base initialized successfully"}
        finally:
            await session.close()
    except Exception as e:
        logger.error(f"Failed to initialize knowledge base: {str(e)}")
        return {"status": "error", "message": str(e)}
