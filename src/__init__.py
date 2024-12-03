"""EADS - Evolutionary Algorithm-based Design System."""

from src.gp_engine import gp_service as gp_engine
from src.nlp import nlp_service as nlp

__version__ = "0.1.0"
__all__ = ["gp_engine", "nlp"]
