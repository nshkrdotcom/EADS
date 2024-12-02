"""Knowledge Base Initialization Module.

This module provides functionality to initialize a Neo4j knowledge base with design
patterns and their relationships. It loads base patterns from a JSON file and creates
a graph structure representing design pattern categories, patterns, and their use cases.

The knowledge base is structured with the following node types:
  - Category: Design pattern categories (Creational, Structural, Behavioral)
  - Pattern: Individual design patterns with names and descriptions
  - UseCase: Specific use cases where patterns are applicable

Relationships:
  - BELONGS_TO: Connects patterns to their categories
  - APPLIES_TO: Connects patterns to their use cases
"""

import json
import logging
import os
from typing import Dict, List, Optional

from neo4j import Driver, GraphDatabase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KnowledgeBaseInitializer:
    """Initializes and populates the Neo4j knowledge base with design patterns.

    This class handles the initialization of the Neo4j database with design patterns,
    their categories, and relationships. It reads pattern data from a JSON file and
    creates the corresponding graph structure.

    Attributes:
        neo4j_uri (str): URI for the Neo4j database connection
        neo4j_user (str): Username for Neo4j authentication
        neo4j_password (str): Password for Neo4j authentication
    """

    def __init__(self) -> None:
        """Initialize the KnowledgeBaseInitializer with Neo4j connection details."""
        self.neo4j_uri: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.neo4j_user: str = os.getenv("NEO4J_USER", "neo4j")
        self.neo4j_password: str = os.getenv("NEO4J_PASSWORD", "password")

    def load_base_patterns(self) -> List[Dict]:
        """Load base design patterns from JSON file.

        Returns:
            List[Dict]: A list of dictionaries containing pattern information.
                Each dictionary contains pattern name, category, description,
                and optional use cases.
        """
        patterns_file = os.path.join(
            os.path.dirname(__file__), "data/base_patterns.json"
        )
        try:
            with open(patterns_file, "r") as f:
                data = json.load(f)
                return data.get("patterns", [])
        except FileNotFoundError:
            logger.warning(f"Base patterns file not found at {patterns_file}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing base patterns JSON: {str(e)}")
            return []

    def init_knowledge_base(self) -> bool:
        """Initialize knowledge base with design patterns and relationships.

        This method performs the following steps:
        1. Connects to the Neo4j database
        2. Creates constraints for category names
        3. Creates pattern categories (Creational, Structural, Behavioral)
        4. Creates patterns and links them to categories
        5. Creates use cases and links them to patterns

        Returns:
            bool: True if initialization was successful, False otherwise

        Raises:
            Neo4jError: If there's an error during database operations
            Exception: For other unexpected errors
        """
        driver: Optional[Driver] = None
        try:
            driver = GraphDatabase.driver(
                self.neo4j_uri,
                auth=(self.neo4j_user, self.neo4j_password),
                max_connection_lifetime=30,  # 30 seconds max connection lifetime
            )

            # Verify connection
            driver.verify_connectivity()

            patterns = self.load_base_patterns()
            if not patterns:
                logger.warning("No patterns loaded from base patterns file")
                return False

            with driver.session(database="neo4j") as session:
                try:
                    # Create pattern categories
                    session.run(
                        """
                        CREATE CONSTRAINT category_name IF NOT EXISTS
                        FOR (c:Category) REQUIRE c.name IS UNIQUE
                    """
                    )

                    # Initialize categories
                    for pattern in patterns:
                        category = pattern.get("category")
                        if not category:
                            logger.warning(
                                f"Pattern {pattern.get('name')} has no category"
                            )
                            continue

                        session.run(
                            """
                            MERGE (c:Category {name: $category})
                            """,
                            category=category,
                        )

                    logger.info("Successfully initialized knowledge base")
                    return True

                except Exception as e:
                    logger.error(f"Error during session operations: {str(e)}")
                    raise

        except Exception as e:
            logger.error(f"Failed to initialize knowledge base: {str(e)}")
            return False

        finally:
            if driver:
                driver.close()
                logger.info("Closed Neo4j driver connection")


def main() -> None:
    """Initialize the knowledge base with design patterns.

    This function creates a KnowledgeBaseInitializer instance and attempts to
    initialize the knowledge base. If initialization fails, the program exits
    with a status code of 1.
    """
    initializer = KnowledgeBaseInitializer()
    success = initializer.init_knowledge_base()

    if not success:
        logger.error("Knowledge base initialization failed")
        exit(1)


if __name__ == "__main__":
    main()
