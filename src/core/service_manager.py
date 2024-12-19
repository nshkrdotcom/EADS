"""Core service manager for EADS."""

import logging
from contextlib import contextmanager
from typing import Generator, Optional

import neo4j
import ray
import weaviate
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session, sessionmaker

from config.core_config import CoreConfig

logger = logging.getLogger(__name__)


class ServiceManager:
    """Manages core services for EADS."""

    def __init__(self, config: CoreConfig):
        """Initialize service manager.

        Args:
            config: Core configuration
        """
        self.config = config
        self._neo4j_driver: Optional[neo4j.Driver] = None
        self._weaviate_client: Optional[weaviate.Client] = None
        self._db_session_maker: Optional[sessionmaker] = None

    def initialize(self) -> None:
        """Initialize all core services."""
        self._init_ray()
        self._init_neo4j()
        self._init_weaviate()
        self._init_postgres()

    def shutdown(self) -> None:
        """Shutdown all core services."""
        if self._neo4j_driver:
            self._neo4j_driver.close()
        if ray.is_initialized():
            ray.shutdown()

    def _init_ray(self) -> None:
        """Initialize Ray."""
        if not ray.is_initialized():
            ray.init(
                address=self.config.ray.address,
                namespace=self.config.ray.namespace,
                num_cpus=self.config.ray.num_cpus,
                num_gpus=self.config.ray.num_gpus,
            )
            logger.info("Ray initialized")

    def _init_neo4j(self) -> None:
        """Initialize Neo4j connection."""
        self._neo4j_driver = neo4j.GraphDatabase.driver(
            self.config.neo4j.uri,
            auth=(self.config.neo4j.username, self.config.neo4j.password),
        )
        logger.info("Neo4j connection established")

    def _init_weaviate(self) -> None:
        """Initialize Weaviate client."""
        auth_config = None
        if self.config.weaviate.api_key:
            auth_config = weaviate.auth.AuthApiKey(api_key=self.config.weaviate.api_key)

        self._weaviate_client = weaviate.Client(
            url=self.config.weaviate.url,
            auth_client_secret=auth_config,
            timeout_config=self.config.weaviate.timeout_config,
        )
        logger.info("Weaviate client initialized")

    def _init_postgres(self) -> None:
        """Initialize PostgreSQL connection."""
        pg_config = self.config.postgres
        db_url = URL.create(
            "postgresql",
            username=pg_config.username,
            password=pg_config.password,
            host=pg_config.host,
            port=pg_config.port,
            database=pg_config.database,
        )
        engine = create_engine(db_url)
        self._db_session_maker = sessionmaker(bind=engine)
        logger.info("PostgreSQL connection established")

    @property
    def neo4j(self) -> neo4j.Driver:
        """Get Neo4j driver.

        Returns:
            neo4j.Driver: Neo4j driver instance
        """
        if not self._neo4j_driver:
            raise RuntimeError("Neo4j driver not initialized")
        return self._neo4j_driver

    @property
    def weaviate(self) -> weaviate.Client:
        """Get Weaviate client.

        Returns:
            weaviate.Client: Weaviate client instance
        """
        if not self._weaviate_client:
            raise RuntimeError("Weaviate client not initialized")
        return self._weaviate_client

    @contextmanager
    def db_session(self) -> Generator[Session, None, None]:
        """Get database session context manager.

        Yields:
            Session: SQLAlchemy session
        """
        if not self._db_session_maker:
            raise RuntimeError("Database session maker not initialized")

        session = self._db_session_maker()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
