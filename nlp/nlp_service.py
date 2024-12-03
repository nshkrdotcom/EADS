"""NLP Service module for text analysis and pattern matching."""

import logging
import logging.config
import sys
from typing import Any, Dict, List

import torch
import uvicorn
from fastapi import FastAPI, HTTPException, status
from neo4j import GraphDatabase

from ..config.settings import (
    LOGGING_CONFIG,
    MODEL_NAME,
    NEO4J_PASSWORD,
    NEO4J_URI,
    NEO4J_USER,
)

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="NLP Service",
    description="A service for natural language processing",
    version="1.0.0",
)

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


@app.on_event("shutdown")  # type: ignore[misc]
async def shutdown_event() -> None:
    """Handle shutdown event."""
    logger.info("Shutting down NLP service")
    if neo4j_driver:
        neo4j_driver.close()
        logger.info("Closed Neo4j connection")


@app.get("/shutdown", response_model=Dict[str, str])  # type: ignore[misc]
async def shutdown() -> Dict[str, str]:
    """Shutdown endpoint."""
    return {"status": "Shutting down"}


@app.get("/", response_model=Dict[str, str])  # type: ignore[misc]
async def read_root() -> Dict[str, str]:
    """Root endpoint."""
    return {"status": "NLP service is running"}


@app.post("/encode", response_model=Dict[str, List[float]])  # type: ignore[misc]
async def encode_text(text: str) -> Dict[str, List[float]]:
    """Encode text into vector representation.

    Args:
        text: Input text to encode

    Returns:
        Dict[str, List[float]]: Encoded vector
    """
    try:
        inputs = tokenizer(
            text,
            padding=True,
            truncation=True,
            return_tensors="pt",
        )

        with torch.no_grad():
            outputs = model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)

        return {"vector": embeddings[0].tolist()}
    except Exception as e:
        logger.error(f"Error encoding text: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze", response_model=Dict[str, Any])  # type: ignore[misc]
async def analyze_pattern(code: str) -> Dict[str, Any]:
    """Analyze a code pattern.

    Args:
        code: Code pattern to analyze

    Returns:
        Dict[str, Any]: Analysis results
    """
    try:
        encoded = await encode_text(code)
        embeddings = encoded["vector"]

        if not neo4j_driver:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection not available",
            )

        with neo4j_driver.session() as session:
            result = session.run(
                """
                MATCH (p:Pattern)
                WITH p, gds.similarity.cosine($embedding, p.embedding) as similarity
                WHERE similarity > 0.8
                RETURN p.name, p.description, similarity
                ORDER BY similarity DESC
                LIMIT 5
                """,
                embedding=embeddings,
            )
            patterns = [dict(record) for record in result]

        return {
            "status": "success",
            "patterns": patterns,
        }
    except Exception as e:
        logger.error(f"Error analyzing pattern: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        workers=1,
    )
