"""Configuration module for EADS."""

from config.settings import (
    NEO4J_PASSWORD,
    NEO4J_URI,
    NEO4J_USER,
    PG_DB,
    PG_HOST,
    PG_PASSWORD,
    PG_PORT,
    PG_USER,
)

__all__ = [
    "NEO4J_URI",
    "NEO4J_USER",
    "NEO4J_PASSWORD",
    "PG_HOST",
    "PG_PORT",
    "PG_USER",
    "PG_PASSWORD",
    "PG_DB",
]
