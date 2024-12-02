"""NLP service module."""

import logging
import sys
from typing import Any, Dict, List, Optional

import torch
import uvicorn
from fastapi import FastAPI, HTTPException, status
from neo4j import GraphDatabase
from transformers import AutoModel, AutoTokenizer

from config.settings import (
    LOGGING_CONFIG,
    MODEL_NAME,
    NEO4J_PASSWORD,
    NEO4J_URI,
    NEO4J_USER,
)
from error_handling.error_handler import handle_exception

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="NLP Service",
    description="A service for code analysis using NLP techniques",
    version="1.0.0",
)

# Initialize tokenizer and model
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME)
    logger.info(f"Successfully loaded {MODEL_NAME} model and tokenizer")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    sys.exit(1)

# Neo4j connection configuration
neo4j_driver: Optional[GraphDatabase.driver] = None

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


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Clean up resources when shutting down."""
    if neo4j_driver:
        neo4j_driver.close()
        logger.info("Closed Neo4j connection")


@app.on_event("shutdown")
async def shutdown() -> None:
    """Shutdown event handler."""
    logger.info("Shutting down NLP service")


@app.get("/", response_model=Dict[str, str])
async def read_root() -> Dict[str, str]:
    """Root endpoint."""
    return {"message": "NLP Service is running"}


@app.post("/encode", response_model=Dict[str, List[float]])
async def encode_text(text: str) -> Dict[str, List[float]]:
    """Encode text using the model."""
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
        logger.error(f"Failed to encode text: {str(e)}")
        return handle_exception(e)


@app.post("/analyze", response_model=Dict[str, Any])
async def analyze_pattern(code: str) -> Dict[str, Any]:
    """Analyze code patterns by comparing with stored patterns in Neo4j."""
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
        logger.error(f"Failed to analyze pattern: {str(e)}")
        return handle_exception(e)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        workers=1,
    )
