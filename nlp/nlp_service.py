"""Natural Language Processing Service for Code Analysis.

This module provides a FastAPI service for encoding and analyzing code patterns.
It uses the CodeBERT model for generating embeddings and provides REST API
endpoints for various NLP operations.
"""

import logging
import sys
from typing import Dict, List, Optional, Union

import torch
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from neo4j import GraphDatabase, Neo4jDriver
from transformers import AutoModel, AutoTokenizer

from config.settings import API_CONFIG, DB_CONFIG, LOGGING_CONFIG, NLP_CONFIG

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="NLP Service",
    description="A service for code analysis using NLP techniques",
    version="1.0.0",
)

# Initialize tokenizer and model
try:
    MODEL_NAME = NLP_CONFIG["model_name"]
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME)
    logger.info(f"Successfully loaded {MODEL_NAME} model and tokenizer")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    logger.error(f"Exiting due to error: {str(e)}")
    sys.exit(1)

# Neo4j connection configuration
neo4j_config = DB_CONFIG["neo4j"]
neo4j_driver: Optional[Neo4jDriver] = None

try:
    neo4j_driver = GraphDatabase.driver(
        neo4j_config["uri"],
        auth=(neo4j_config["user"], neo4j_config["password"]),
        max_connection_lifetime=neo4j_config["max_connection_lifetime"],
    )
    neo4j_driver.verify_connectivity()
    logger.info("Successfully connected to Neo4j database")
except Exception as e:
    logger.error(f"Failed to connect to Neo4j: {str(e)}")
    logger.error(f"Exiting due to error: {str(e)}")
    sys.exit(1)


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources when shutting down."""
    if neo4j_driver:
        neo4j_driver.close()
        logger.info("Closed Neo4j connection")


@app.get("/")
def read_root() -> Dict[str, str]:
    """Check if the NLP service is running.

    Returns:
        Dict[str, str]: A dictionary containing the service status
    """
    return {"status": "NLP Service is running"}


@app.post("/encode")
async def encode_text(text: str) -> Dict[str, Union[List[float], str]]:
    """Encode text using the CodeBERT model.

    Args:
        text: The text to encode

    Returns:
        Dict containing the encoded vector and status

    Raises:
        HTTPException: If encoding fails
    """
    try:
        # Tokenize and encode
        inputs = tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=NLP_CONFIG["max_tokens"],
            return_tensors="pt",
        )

        with torch.no_grad():
            outputs = model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)

        return {"vector": embeddings[0].tolist(), "status": "success"}

    except Exception as e:
        logger.error(f"Error encoding text: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to encode text: {str(e)}",
        )


@app.post("/analyze")
async def analyze_pattern(
    code: str,
) -> Dict[str, Union[List[Dict[str, str]], List[float]]]:
    """Analyze code patterns by comparing with stored patterns in Neo4j.

    Args:
        code: The code snippet to analyze

    Returns:
        Dict containing similar patterns and embeddings

    Raises:
        HTTPException: If pattern analysis fails
    """
    try:
        # Get embeddings for the input code
        encoded = await encode_text(code)
        embeddings = encoded["vector"]

        # Query Neo4j for similar patterns
        if not neo4j_driver:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection not available",
            )

        with neo4j_driver.session() as session:
            result = session.run(
                """
                MATCH (p:Pattern)
                WITH p, gds.similarity.cosine($embeddings, p.embeddings) AS similarity
                WHERE similarity > 0.7
                RETURN p.name AS name, p.description AS description, similarity
                ORDER BY similarity DESC
                LIMIT 5
                """,
                embeddings=embeddings,
            )

            patterns = [
                {
                    "name": record["name"],
                    "description": record["description"],
                    "similarity": record["similarity"],
                }
                for record in result
            ]

        return {"patterns": patterns, "embeddings": embeddings}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing pattern: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze pattern: {str(e)}",
        )


if __name__ == "__main__":
    nlp_config = API_CONFIG["nlp_service"]
    uvicorn.run(
        app,
        host=nlp_config["host"],
        port=nlp_config["port"],
        workers=nlp_config["workers"],
    )
