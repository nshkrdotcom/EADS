"""NLP module for code analysis."""

from src.nlp.nlp_service import analyze_code as analyze_pattern
from src.nlp.nlp_service import app, encode_text

__all__ = ["app", "encode_text", "analyze_pattern"]
