"""Knowledge base initialization module."""

import logging
import logging.config
from typing import Any, Dict, List, Sequence

from neo4j import Driver

from ..config.settings import LOGGING_CONFIG

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def initialize_knowledge_base(driver: Driver) -> Dict[str, Any]:
    """Initialize the knowledge base with design patterns.

    Args:
        driver: Neo4j driver instance

    Returns:
        Dictionary containing initialization status and count of patterns added
    """
    try:
        with driver.session() as session:
            # Create constraints
            session.run(
                """
                CREATE CONSTRAINT pattern_name IF NOT EXISTS
                FOR (p:Pattern) REQUIRE p.name IS UNIQUE
                """
            )

            # Add initial patterns
            result = session.run(
                """
                UNWIND $patterns AS pattern
                MERGE (p:Pattern {name: pattern.name})
                SET p.description = pattern.description,
                    p.code = pattern.code,
                    p.embedding = pattern.embedding
                RETURN count(p) as count
                """,
                patterns=get_initial_patterns(),
            )
            patterns_added = result.single()["count"]

            logger.info(f"Added {patterns_added} patterns to knowledge base")
            return {
                "status": "success",
                "patterns_added": patterns_added,
            }

    except Exception as e:
        logger.error(f"Failed to initialize knowledge base: {str(e)}")
        return {
            "status": "error",
            "message": str(e),
        }


def get_initial_patterns() -> List[Dict[str, Sequence[Any]]]:
    """Get initial patterns to populate the knowledge base.

    Returns:
        List[Dict[str, Sequence[Any]]]: List of initial patterns
    """
    # TODO: Add more patterns
    return [
        {
            "name": "Basic Loop",
            "elements": ["for", "in", "range"],
        },
        {
            "name": "Conditional",
            "elements": ["if", "else", "elif"],
        },
    ]
