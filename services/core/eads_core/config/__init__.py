"""Configuration module for EADS."""
from typing import Any, Dict

from .settings import LOGGING_CONFIG, CoreConfig


def load_config() -> Dict[str, Any]:
    """Load core service configuration.

    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    config = CoreConfig()
    return {
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
        "logging": LOGGING_CONFIG,
    }


__all__ = ["load_config"]
