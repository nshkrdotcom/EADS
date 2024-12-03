"""NLP Service module for text analysis and pattern matching."""

import logging
import logging.config
import sys
from contextlib import asynccontextmanager
from typing import Any, Dict, List, AsyncGenerator

import torch
import uvicorn
from fastapi import FastAPI, HTTPException, status
from neo4j import GraphDatabase
from pydantic import BaseModel

from src.config.settings import (
    LOGGING_CONFIG,
    MODEL_NAME,
    NEO4J_PASSWORD,
    NEO4J_URI,
    NEO4J_USER,
)

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# Initialize tokenizer and model
try:
    from transformers import AutoModel, AutoTokenizer

    tokenizer: AutoTokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model: AutoModel = AutoModel.from_pretrained(MODEL_NAME)
    logger.info(f"Successfully loaded {MODEL_NAME} model and tokenizer")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    sys.exit(1)

# Neo4j connection configuration
neo4j_driver: GraphDatabase.driver = None

try:
    neo4j_driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASSWORD),
    )
    neo4j_driver.verify_connectivity()
    logger.info("Successfully connected to Neo4j database")
except Exception as e:
    logger.error(f"Failed to connect to Neo4j: {str(e)}")
    sys.exit(1)


# Request Models
class TextRequest(BaseModel):
    text: str

class CodeRequest(BaseModel):
    code: str


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Handle application lifespan events.

    Args:
        app: FastAPI application instance

    Yields:
        None
    """
    # Startup
    yield
    # Shutdown
    logger.info("Shutting down NLP service")
    if neo4j_driver:
        neo4j_driver.close()
        logger.info("Closed Neo4j connection")


app = FastAPI(
    title="NLP Service",
    description="A service for natural language processing",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/shutdown", response_model=Dict[str, str])  # type: ignore[misc]
async def shutdown() -> Dict[str, str]:
    """Shutdown endpoint."""
    return {"status": "Shutting down"}


@app.get("/", response_model=Dict[str, str])  # type: ignore[misc]
async def read_root() -> Dict[str, str]:
    """Root endpoint."""
    return {"message": "NLP Service is running"}


@app.post("/encode", response_model=Dict[str, Any])  # type: ignore[misc]
async def encode_text(request: TextRequest) -> Dict[str, Any]:
    """Encode text into vector representation.

    Args:
        request: Request containing text to encode

    Returns:
        Dict[str, Any]: Encoded vector and status
    """
    try:
        inputs = tokenizer(
            request.text,
            padding=True,
            truncation=True,
            return_tensors="pt",
        )

        with torch.no_grad():
            outputs = model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)

        return {
            "status": "success",
            "encoding": embeddings[0].tolist()
        }
    except Exception as e:
        logger.error(f"Error encoding text: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@app.post("/analyze", response_model=Dict[str, Any])  # type: ignore[misc]
async def analyze_pattern(request: CodeRequest) -> Dict[str, Any]:
    """Analyze a code pattern.

    Args:
        request: Request containing code to analyze

    Returns:
        Dict[str, Any]: Analysis results
    """
    try:
        # Encode the code using our model
        inputs = tokenizer(
            request.code,
            padding=True,
            truncation=True,
            return_tensors="pt",
        )

        with torch.no_grad():
            outputs = model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)

        return {
            "status": "success",
            "patterns": embeddings[0].tolist()
        }
    except Exception as e:
        logger.error(f"Error analyzing pattern: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


if __name__ == "__main__":
    uvicorn.run(
        "src.nlp.nlp_service:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
    )
