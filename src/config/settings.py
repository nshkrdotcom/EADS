"""Configuration settings for EADS."""

import logging
import os
from typing import Dict, Any

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Neo4j settings
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# NLP Model settings
MODEL_NAME = os.getenv("MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

# Genetic Programming Configuration
GP_CONFIG: Dict[str, Any] = {
    "population_size": int(os.getenv("GP_POPULATION_SIZE", "100")),
    "generations": int(os.getenv("GP_GENERATIONS", "50")),
    "mutation_rate": float(os.getenv("GP_MUTATION_RATE", "0.1")),
    "crossover_rate": float(os.getenv("GP_CROSSOVER_RATE", "0.7")),
    "tournament_size": int(os.getenv("GP_TOURNAMENT_SIZE", "3")),
    "max_depth": int(os.getenv("GP_MAX_DEPTH", "17")),
}

# Logging Configuration
LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "eads.log",
            "formatter": "default",
            "level": "DEBUG",
        },
    },
    "root": {
        "level": os.getenv("LOG_LEVEL", "INFO"),
        "handlers": ["console", "file"],
    },
}
