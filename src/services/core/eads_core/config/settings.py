"""Configuration settings for the EADS application."""
from typing import Any, Dict

from dotenv import load_dotenv
from pydantic import BaseSettings

# Load environment variables from .env file
load_dotenv()


class CoreConfig(BaseSettings):
    """Core service configuration settings.

    Attributes:
        environment: Runtime environment (development, staging, production)
        version: Service version
        log_level: Logging level (debug, info, warning, error)
    """

    environment: str = "development"
    version: str = "dev"
    log_level: str = "info"

    # Neo4j settings
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password"

    # NLP Model settings
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Genetic Programming settings
    gp_population_size: int = 100
    gp_generations: int = 50
    gp_mutation_rate: float = 0.1
    gp_crossover_rate: float = 0.7

    class Config:
        """Pydantic config class."""

        env_prefix = "EADS_"
        case_sensitive = False


def load_config() -> Dict[str, Any]:
    """Load core service configuration.

    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    config = CoreConfig()
    return {
        "environment": config.environment,
        "version": config.version,
        "log_level": config.log_level,
        "neo4j": {
            "uri": config.neo4j_uri,
            "user": config.neo4j_user,
            "password": config.neo4j_password,
        },
        "model": {"name": config.model_name},
        "gp": {
            "population_size": config.gp_population_size,
            "generations": config.gp_generations,
            "mutation_rate": config.gp_mutation_rate,
            "crossover_rate": config.gp_crossover_rate,
        },
    }


# Default logging configuration
LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {"handlers": ["default"], "level": "INFO", "propagate": True},
    },
}
