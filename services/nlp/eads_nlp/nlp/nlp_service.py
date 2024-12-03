"""NLP service for code analysis and pattern matching."""

import logging
from typing import Any, Dict, List

import uvicorn
from eads_nlp.config.settings import MODEL_NAME
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

app = FastAPI()
model = SentenceTransformer(MODEL_NAME)


class TextRequest(BaseModel):
    """Request model for text encoding endpoint."""

    text: str


class CodeRequest(BaseModel):
    """Request model for code analysis endpoint."""

    code: str


@app.get("/", response_model=Dict[str, str])
async def root() -> Dict[str, str]:
    """Root endpoint to verify service status.

    Returns:
        Dict[str, str]: Service status message
    """
    return {"message": "NLP Service is running"}


@app.post("/encode", response_model=Dict[str, Any])
async def encode_text(request: TextRequest) -> Dict[str, Any]:
    """Encode text using the sentence transformer model.

    Args:
        request: Text encoding request containing the text to encode

    Returns:
        Dict[str, Any]: Encoded text representation
    """
    try:
        text_embedding = model.encode(request.text)
        return {"encoding": text_embedding.tolist()}
    except Exception as e:
        logger.error(f"Error encoding text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze", response_model=Dict[str, Any])
async def analyze_code(request: CodeRequest) -> Dict[str, Any]:
    """Analyze code to identify patterns and potential improvements.

    Args:
        request: Code analysis request containing the code to analyze

    Returns:
        Dict[str, Any]: Analysis results including identified patterns
    """
    try:
        # Placeholder for actual code analysis logic
        patterns: List[str] = ["pattern1", "pattern2"]
        return {"patterns": patterns}
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
