"""Natural Language Processing Service for Code Analysis.

This module provides a FastAPI service for encoding and analyzing code patterns.
It uses the CodeBERT model for generating embeddings and provides REST API
endpoints for various NLP operations.
"""

import os
from typing import Dict, List, Union

import torch
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from neo4j import GraphDatabase
from transformers import AutoModel, AutoTokenizer

# Load environment variables
load_dotenv()

app = FastAPI(
    title="NLP Service",
    description="A service for code analysis using NLP techniques",
    version="1.0.0"
)

# Initialize tokenizer and model
MODEL_NAME = "microsoft/codebert-base"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

# Neo4j connection configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

neo4j_driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)


@app.get("/")
def read_root() -> Dict[str, str]:
    """Check if the NLP service is running.

    Returns:
        Dict[str, str]: A dictionary containing the service status
    """
    return {"status": "NLP Service is running"}


@app.post("/encode")
async def encode_text(text: str) -> Dict[str, Union[List[float], str]]:
    """Encode input text using the CodeBERT model.

    Args:
        text (str): The input text to encode

    Returns:
        Dict[str, Union[List[float], str]]: A dictionary containing the
            embeddings and status

    Raises:
        HTTPException: If encoding fails
    """
    try:
        # Tokenize and encode text
        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )
        with torch.no_grad():
            outputs = model(**inputs)

        # Get embeddings (use mean pooling)
        embeddings = outputs.last_hidden_state.mean(dim=1)

        return {"embeddings": embeddings[0].tolist(), "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze_pattern")
async def analyze_pattern(
    code: str
) -> Dict[str, Union[List[Dict[str, str]], List[float]]]:
    """Analyze code patterns by comparing with stored patterns in Neo4j.

    Args:
        code (str): The code snippet to analyze

    Returns:
        Dict[str, Union[List[Dict[str, str]], List[float]]]: A dictionary
            containing similar patterns and embeddings

    Raises:
        HTTPException: If pattern analysis fails
    """
    try:
        # Encode the code
        inputs = tokenizer(
            code,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )
        with torch.no_grad():
            outputs = model(**inputs)

        embeddings = outputs.last_hidden_state.mean(dim=1)

        # Query Neo4j for similar patterns
        with neo4j_driver.session() as session:
            result = session.run(
                """
                MATCH (p:Pattern)
                RETURN p.name, p.description
                LIMIT 5
                """
            )
            patterns = [
                {"name": record["p.name"], "description": record["p.description"]}
                for record in result
            ]

        return {"patterns": patterns, "embeddings": embeddings[0].tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
