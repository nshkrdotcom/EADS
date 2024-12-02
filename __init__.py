"""EADS - Evolutionary Algorithm-based Design System.

This package provides tools and services for evolving code designs using
genetic programming and natural language processing techniques.
"""

__version__ = "0.1.0"
__author__ = "EADS Team"
__email__ = "team@eads.com"

from . import (
    config,
    error_handling,
    gp_engine,
    init,
    nlp,
)

__all__ = [
    "config",
    "error_handling",
    "gp_engine",
    "init",
    "nlp",
]
