"""Core configuration for EADS services."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Neo4jConfig:
    """Neo4j graph database configuration."""

    uri: str
    username: str
    password: str
    database: str = "neo4j"


@dataclass
class WeaviateConfig:
    """Weaviate vector database configuration."""

    url: str
    api_key: Optional[str] = None
    batch_size: int = 100
    timeout_config: int = 60


@dataclass
class RayConfig:
    """Ray distributed computing configuration."""

    address: Optional[str] = None
    namespace: str = "eads"
    num_cpus: Optional[int] = None
    num_gpus: Optional[int] = None


@dataclass
class PostgresConfig:
    """PostgreSQL database configuration."""

    host: str
    port: int
    database: str
    username: str
    password: str


@dataclass
class CoreConfig:
    """Core configuration for all EADS services."""

    neo4j: Neo4jConfig
    weaviate: WeaviateConfig
    ray: RayConfig
    postgres: PostgresConfig
    debug: bool = False
