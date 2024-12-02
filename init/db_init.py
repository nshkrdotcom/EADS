"""Database initialization module for EADS.

This module handles the initialization and setup of database connections,
including PostgreSQL and Neo4j databases.
"""

import logging
import os
import time
from typing import Any, Dict, Optional, Tuple, Union

import pinecone
import psycopg2
from neo4j import GraphDatabase, Driver
from psycopg2.extensions import connection as PGConnection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseInitializer:
    """Handle initialization of database connections and schema setup."""

    def __init__(
        self,
        pg_host: str,
        pg_port: int,
        pg_user: str,
        pg_password: str,
        pg_db: str,
        neo4j_uri: str,
        neo4j_user: str,
        neo4j_password: str,
    ) -> None:
        """Initialize the database connection parameters.

        Args:
            pg_host: PostgreSQL host address
            pg_port: PostgreSQL port number
            pg_user: PostgreSQL username
            pg_password: PostgreSQL password
            pg_db: PostgreSQL database name
            neo4j_uri: Neo4j connection URI
            neo4j_user: Neo4j username
            neo4j_password: Neo4j password
        """
        self.pg_params = {
            "host": pg_host,
            "port": pg_port,
            "user": pg_user,
            "password": pg_password,
            "database": pg_db,
        }
        self.neo4j_uri = neo4j_uri
        self.neo4j_auth = (neo4j_user, neo4j_password)

    def wait_for_postgres(
        self, max_attempts: int = 5, delay: int = 2
    ) -> Tuple[bool, Optional[PGConnection]]:
        """Wait for PostgreSQL to become available.

        Args:
            max_attempts: Maximum number of connection attempts
            delay: Delay between attempts in seconds

        Returns:
            Tuple[bool, Optional[PGConnection]]: Success status and connection
        """
        for attempt in range(max_attempts):
            try:
                conn = psycopg2.connect(**self.pg_params)
                return True, conn
            except psycopg2.Error as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_attempts - 1:
                    time.sleep(delay)
        return False, None

    def wait_for_neo4j(
        self, max_attempts: int = 5, delay: int = 2
    ) -> Tuple[bool, Optional[Driver]]:
        """Wait for Neo4j to become available.

        Args:
            max_attempts: Maximum number of connection attempts
            delay: Delay between attempts in seconds

        Returns:
            Tuple[bool, Optional[Driver]]: Success status and driver
        """
        for attempt in range(max_attempts):
            try:
                driver = GraphDatabase.driver(
                    self.neo4j_uri, auth=self.neo4j_auth
                )
                driver.verify_connectivity()
                return True, driver
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_attempts - 1:
                    time.sleep(delay)
        return False, None

    def initialize_databases(self) -> bool:
        """Initialize all database connections and schemas.

        Returns:
            bool: True if initialization was successful, False otherwise
        """
        # Connect to PostgreSQL
        pg_success, pg_conn = self.wait_for_postgres()
        if not pg_success or pg_conn is None:
            logger.error("Failed to connect to PostgreSQL")
            return False

        # Connect to Neo4j
        neo4j_success, neo4j_driver = self.wait_for_neo4j()
        if not neo4j_success or neo4j_driver is None:
            logger.error("Failed to connect to Neo4j")
            if pg_conn:
                pg_conn.close()
            return False

        try:
            # Initialize Pinecone if API key is available
            pinecone_key = os.getenv("PINECONE_API_KEY")
            if pinecone_key:
                pinecone.init(api_key=pinecone_key)
                _ = pinecone.list_indexes()
            else:
                logger.warning("Pinecone API key not found")

            # Create tables for metadata tracking
            with pg_conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS code_snippets (
                        id SERIAL PRIMARY KEY,
                        content TEXT NOT NULL,
                        language VARCHAR(50),
                        pattern_name VARCHAR(100),
                        embedding_id VARCHAR(100),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        metadata JSONB
                    )
                    """
                )
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS evolution_history (
                        id SERIAL PRIMARY KEY,
                        snippet_id INTEGER REFERENCES code_snippets(id),
                        parent_id INTEGER REFERENCES code_snippets(id),
                        fitness_score FLOAT,
                        generation INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        metadata JSONB
                    )
                    """
                )
                pg_conn.commit()

            # Create constraints and indexes
            with neo4j_driver.session() as session:
                session.run(
                    """
                    CREATE CONSTRAINT unique_concept IF NOT EXISTS
                    FOR (c:Concept) REQUIRE c.name IS UNIQUE
                    """
                )

            logger.info("Database initialization completed successfully")
            return True

        except Exception as e:
            logger.error(f"Error during initialization: {e}")
            return False
        finally:
            if pg_conn:
                pg_conn.close()
            if neo4j_driver:
                neo4j_driver.close()


def init_databases(config: Dict[str, Any]) -> bool:
    """Initialize databases with the provided configuration.

    Args:
        config: Dictionary containing database configuration parameters

    Returns:
        bool: True if initialization was successful, False otherwise
    """
    try:
        initializer = DatabaseInitializer(
            pg_host=config.get("PG_HOST", "localhost"),
            pg_port=config.get("PG_PORT", 5432),
            pg_user=config.get("PG_USER", "postgres"),
            pg_password=config.get("PG_PASSWORD", "password"),
            pg_db=config.get("PG_DB", "eads"),
            neo4j_uri=config.get("NEO4J_URI", "bolt://localhost:7687"),
            neo4j_user=config.get("NEO4J_USER", "neo4j"),
            neo4j_password=config.get("NEO4J_PASSWORD", "password"),
        )
        return initializer.initialize_databases()
    except Exception as e:
        logger.error(f"Failed to initialize databases: {e}")
        return False


def main() -> None:
    """Initialize the databases with default configuration."""
    config = {
        "PG_HOST": os.getenv("PG_HOST", "localhost"),
        "PG_PORT": int(os.getenv("PG_PORT", "5432")),
        "PG_USER": os.getenv("PG_USER", "postgres"),
        "PG_PASSWORD": os.getenv("PG_PASSWORD", "password"),
        "PG_DB": os.getenv("PG_DB", "eads"),
        "NEO4J_URI": os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        "NEO4J_USER": os.getenv("NEO4J_USER", "neo4j"),
        "NEO4J_PASSWORD": os.getenv("NEO4J_PASSWORD", "password"),
    }
    success = init_databases(config)
    if not success:
        logger.error("Database initialization failed")
        exit(1)


if __name__ == "__main__":
    main()
