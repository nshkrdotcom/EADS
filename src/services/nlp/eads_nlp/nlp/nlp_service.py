"""NLP service for code analysis and pattern matching."""

import logging
from typing import Any, Dict, List, Tuple

import numpy as np
import uvicorn
from eads_nlp.config.settings import MODEL_NAME
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from ..logging import log_operation

logger = logging.getLogger(__name__)

app = FastAPI()
model = SentenceTransformer(MODEL_NAME)


class TextRequest(BaseModel):
    """Request model for text encoding endpoint."""

    text: str


class CodeRequest(BaseModel):
    """Request model for code analysis endpoint."""

    code: str
    pattern: str


def encode_text(text: str) -> np.ndarray:
    """Encode text using the sentence transformer model.

    Args:
        text: Text to encode

    Returns:
        np.ndarray: Encoded text representation
    """
    with log_operation("encode_text_internal", text_length=len(text)) as ctx:
        embedding = model.encode(text)
        ctx.update(embedding_shape=embedding.shape)
        return embedding


def analyze_code(code: str, pattern: str) -> Tuple[float, List[str]]:
    """Analyze code to identify patterns and calculate similarity.

    Args:
        code: Code snippet to analyze
        pattern: Pattern to compare against

    Returns:
        Tuple[float, List[str]]: Similarity score and list of matches
    """
    with log_operation(
        "analyze_code_internal", code_length=len(code), pattern_length=len(pattern)
    ) as ctx:
        # Encode both code and pattern
        code_embedding = encode_text(code)
        pattern_embedding = encode_text(pattern)

        # Calculate cosine similarity
        similarity = float(
            np.dot(code_embedding, pattern_embedding)
            / (np.linalg.norm(code_embedding) * np.linalg.norm(pattern_embedding))
        )

        # For now, return a simple match list
        # TODO: Implement actual pattern matching logic
        matches = ["placeholder_match"] if similarity > 0.5 else []

        ctx.update(similarity=similarity, num_matches=len(matches))
        return similarity, matches


@app.get("/", response_model=Dict[str, str])
async def root() -> Dict[str, str]:
    """Root endpoint to verify service status.

    Returns:
        Dict[str, str]: Service status message
    """
    return {"message": "NLP Service is running"}


@app.post("/encode", response_model=Dict[str, Any])
async def encode_text_endpoint(request: TextRequest) -> Dict[str, Any]:
    """Encode text using the sentence transformer model.

    Args:
        request: Text encoding request containing the text to encode

    Returns:
        Dict[str, Any]: Encoded text representation
    """
    try:
        text_embedding = encode_text(request.text)
        return {"encoding": text_embedding.tolist()}
    except Exception as e:
        logger.error(f"Error encoding text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze", response_model=Dict[str, Any])
async def analyze_code_endpoint(request: CodeRequest) -> Dict[str, Any]:
    """Analyze code to identify patterns and calculate similarity.

    Args:
        request: Code analysis request containing the code to analyze

    Returns:
        Dict[str, Any]: Analysis results including identified patterns
    """
    try:
        similarity, matches = analyze_code(request.code, request.pattern)
        return {"similarity": similarity, "matches": matches}
    except Exception as e:
        logger.error(f"Error analyzing code: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "src.nlp.nlp_service:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
    )
