import logging
import os
import time

import psycopg2
from neo4j import GraphDatabase
from pinecone import Pinecone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseInitializer:
    def __init__(self):
        # Initialize connection parameters from environment variables
        # Use localhost for local development
        self.neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD", "password")

        self.pg_host = os.getenv("POSTGRES_HOST", "localhost")
        self.pg_user = os.getenv("POSTGRES_USER", "postgres")
        self.pg_password = os.getenv("POSTGRES_PASSWORD", "password")
        self.pg_db = os.getenv("POSTGRES_DB", "eads")

        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")

    def wait_for_neo4j(self, max_retries=5, delay=5):
        """Wait for Neo4j to become available"""
        for attempt in range(max_retries):
            try:
                driver = GraphDatabase.driver(
                    self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password)
                )
                with driver.session() as session:
                    session.run("RETURN 1")
                driver.close()
                return True
            except Exception as e:
                logger.warning(
                    f"Waiting for Neo4j (attempt {attempt + 1}/{max_retries}): {str(e)}"
                )
                time.sleep(delay)
        return False

    def wait_for_postgres(self, max_retries=5, delay=5):
        """Wait for PostgreSQL to become available"""
        for attempt in range(max_retries):
            try:
                conn = psycopg2.connect(
                    host=self.pg_host,
                    database=self.pg_db,
                    user=self.pg_user,
                    password=self.pg_password,
                )
                conn.close()
                return True
            except Exception as e:
                logger.warning(
                    f"Waiting for PostgreSQL (attempt {attempt + 1}/{max_retries}): {str(e)}"
                )
                time.sleep(delay)
        return False

    def init_neo4j(self):
        """Initialize Neo4j with base schema for knowledge graph"""
        try:
            driver = GraphDatabase.driver(
                self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password)
            )

            with driver.session() as session:
                # Create constraints and indexes
                session.run(
                    """
                    CREATE CONSTRAINT unique_concept IF NOT EXISTS
                    FOR (c:Concept) REQUIRE c.name IS UNIQUE
                """
                )

                session.run(
                    """
                    CREATE CONSTRAINT unique_pattern IF NOT EXISTS
                    FOR (p:Pattern) REQUIRE p.name IS UNIQUE
                """
                )

                # Create base knowledge graph structure
                session.run(
                    """
                    MERGE (root:Concept {name: 'Software_Development'})
                    MERGE (patterns:Concept {name: 'Design_Patterns'})
                    MERGE (arch:Concept {name: 'Architecture_Patterns'})
                    MERGE (sec:Concept {name: 'Security_Patterns'})
                    MERGE (perf:Concept {name: 'Performance_Patterns'})

                    MERGE (root)-[:INCLUDES]->(patterns)
                    MERGE (root)-[:INCLUDES]->(arch)
                    MERGE (root)-[:INCLUDES]->(sec)
                    MERGE (root)-[:INCLUDES]->(perf)
                """
                )

            logger.info("Neo4j initialization completed successfully")
            return True

        except Exception as e:
            logger.error(f"Error initializing Neo4j: {str(e)}")
            return False

    def init_postgres(self):
        """Initialize PostgreSQL with necessary tables"""
        try:
            conn = psycopg2.connect(
                host=self.pg_host,
                database=self.pg_db,
                user=self.pg_user,
                password=self.pg_password,
            )

            cur = conn.cursor()

            # Create tables for metadata tracking
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

            conn.commit()
            logger.info("PostgreSQL initialization completed successfully")
            return True

        except Exception as e:
            logger.error(f"Error initializing PostgreSQL: {str(e)}")
            return False
        finally:
            if "conn" in locals():
                conn.close()

    def init_pinecone(self):
        """Initialize Pinecone for vector embeddings"""
        try:
            if not self.pinecone_api_key:
                logger.warning("Pinecone API key not found in environment variables")
                return False

            pc = Pinecone(api_key=self.pinecone_api_key)

            # Create index if it doesn't exist
            if "code-embeddings" not in pc.list_indexes():
                pc.create_index(
                    name="code-embeddings",
                    dimension=1536,  # Using OpenAI's embedding dimension
                    metric="cosine",
                )

            logger.info("Pinecone initialization completed successfully")
            return True

        except Exception as e:
            logger.error(f"Error initializing Pinecone: {str(e)}")
            return False


def main():
    initializer = DatabaseInitializer()

    # Wait for services to be ready
    logger.info("Waiting for services to be ready...")
    if not initializer.wait_for_neo4j():
        logger.error("Neo4j is not available after maximum retries")
        return
    if not initializer.wait_for_postgres():
        logger.error("PostgreSQL is not available after maximum retries")
        return

    # Initialize all databases
    neo4j_success = initializer.init_neo4j()
    postgres_success = initializer.init_postgres()

    # Make Pinecone optional
    if (
        initializer.pinecone_api_key
        and initializer.pinecone_api_key != "your_pinecone_api_key"
    ):
        pinecone_success = initializer.init_pinecone()
    else:
        logger.info("Skipping Pinecone initialization (API key not configured)")
        pinecone_success = True  # Don't count it as a failure

    # Only check Neo4j and PostgreSQL for required success
    if all([neo4j_success, postgres_success]):
        logger.info("Required database initializations completed successfully")
    else:
        logger.error("Required database initializations failed. Check logs for details")
        exit(1)


if __name__ == "__main__":
    main()
