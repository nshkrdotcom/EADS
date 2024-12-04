"""Configuration module for EADS."""
from typing import Any, Dict

from .settings import LOGGING_CONFIG, CoreConfig, load_config

__all__ = ["CoreConfig", "load_config", "LOGGING_CONFIG"]
