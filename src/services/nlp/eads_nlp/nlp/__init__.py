"""NLP module for code analysis."""

from .nlp_service import analyze_code as analyze_pattern
from .nlp_service import app, encode_text

__all__ = ["app", "encode_text", "analyze_pattern"]
