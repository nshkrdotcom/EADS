"""Configuration settings for the EADS application."""

import os
from typing import Any, Dict

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Neo4j settings
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# NLP Model settings
MODEL_NAME = os.getenv("MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

# Genetic Programming settings
GP_CONFIG: Dict[str, Any] = {
    "population_size": int(os.getenv("GP_POPULATION_SIZE", "100")),
    "generations": int(os.getenv("GP_GENERATIONS", "50")),
    "mutation_rate": float(os.getenv("GP_MUTATION_RATE", "0.1")),
    "crossover_rate": float(os.getenv("GP_CROSSOVER_RATE", "0.7")),
}

# Logging Configuration
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
