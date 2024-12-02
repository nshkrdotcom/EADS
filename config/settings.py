"""Configuration settings for EADS.

This module contains all configuration settings for the EADS system,
including database connections, API settings, and various parameters
for different components.
"""

import os
from typing import Dict, Any

# Database Settings
DB_CONFIG: Dict[str, Any] = {
    "neo4j": {
        "uri": os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        "user": os.getenv("NEO4J_USER", "neo4j"),
        "password": os.getenv("NEO4J_PASSWORD", "password"),
        "max_connection_lifetime": 30,  # seconds
        "max_connection_pool_size": 50,
    },
    "postgres": {
        "host": os.getenv("PG_HOST", "localhost"),
        "port": int(os.getenv("PG_PORT", "5432")),
        "user": os.getenv("PG_USER", "postgres"),
        "password": os.getenv("PG_PASSWORD", "postgres"),
        "database": os.getenv("PG_DB", "eads"),
        "min_connections": 1,
        "max_connections": 10,
    }
}

# API Settings
API_CONFIG: Dict[str, Any] = {
    "nlp_service": {
        "host": "0.0.0.0",
        "port": 8000,
        "workers": 4,
        "timeout": 60,
    },
    "gp_service": {
        "host": "0.0.0.0",
        "port": 8001,
        "workers": 4,
        "timeout": 120,
    }
}

# Genetic Programming Settings
GP_CONFIG: Dict[str, Any] = {
    "population_size": 100,
    "generations": 50,
    "mutation_rate": 0.2,
    "crossover_rate": 0.8,
    "tournament_size": 3,
}

# NLP Service Settings
NLP_CONFIG: Dict[str, Any] = {
    "model_name": "gpt-3.5-turbo",
    "max_tokens": 1000,
    "temperature": 0.7,
    "batch_size": 32,
}

# Logging Configuration
LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": "eads.log",
            "mode": "a",
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["default", "file"],
            "level": "INFO",
            "propagate": True
        },
    },
}
