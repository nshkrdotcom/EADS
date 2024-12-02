"""Configuration settings for EADS."""

import os
from typing import Optional, Type

# Database Settings
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = int(os.getenv("PG_PORT", "5432"))
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "postgres")
PG_DB = os.getenv("PG_DB", "eads")

# Model Settings
MODEL_NAME = "microsoft/codebert-base"
MODEL_MAX_LENGTH = 512

# Genetic Programming settings
GP_CONFIG = {
    "population_size": 100,
    "generations": 50,
    "mutation_rate": 0.2,
    "crossover_rate": 0.7,
}

# Logging Configuration
LOGGING_CONFIG = {
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


class Settings:
    """Application settings."""

    _instance: Optional["Settings"] = None

    def __init__(self) -> None:
        """Initialize settings."""
        self.neo4j_uri = NEO4J_URI
        self.neo4j_user = NEO4J_USER
        self.neo4j_password = NEO4J_PASSWORD
        self.pg_host = PG_HOST
        self.pg_port = PG_PORT
        self.pg_user = PG_USER
        self.pg_password = PG_PASSWORD
        self.pg_db = PG_DB
        self.model_name = MODEL_NAME
        self.model_max_length = MODEL_MAX_LENGTH
        self.gp_config = GP_CONFIG

    @classmethod
    def get_instance(cls: Type["Settings"]) -> "Settings":
        """Get singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


settings = Settings.get_instance()

__all__ = [
    "settings",
    "Settings",
    "NEO4J_URI",
    "NEO4J_USER",
    "NEO4J_PASSWORD",
    "PG_HOST",
    "PG_PORT",
    "PG_USER",
    "PG_PASSWORD",
    "PG_DB",
    "MODEL_NAME",
    "MODEL_MAX_LENGTH",
    "GP_CONFIG",
    "LOGGING_CONFIG",
]
