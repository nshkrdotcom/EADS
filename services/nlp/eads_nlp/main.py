"""NLP service FastAPI application."""
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .nlp.nlp_service import analyze_code, encode_text
from .vector_store import WeaviateClient, WeaviateConfig

app = FastAPI(title="EADS NLP Service")
config = WeaviateConfig(host="localhost", port=8080)
vector_store = WeaviateClient(config)


class HealthCheck(BaseModel):
    """Health check response model for the NLP service.

    Attributes:
        status (str): The current status of the service
        service (str): The name of the service
        vector_store_ready (bool): Whether the vector store is initialized and ready
    """

    status: str = "healthy"
    service: str = "nlp"
    vector_store_ready: bool = True


class AnalyzeRequest(BaseModel):
    """Request model for code analysis.

    Attributes:
        code (str): The code snippet to analyze
        pattern (str): The pattern to analyze the code against
    """

    code: str
    pattern: str


class AnalyzeResponse(BaseModel):
    """Response model for code analysis results.

    Attributes:
        similarity (float): The similarity score of the analyzed code
        matches (List[str]): The list of matches found in the analyzed code
    """

    similarity: float
    matches: List[str]


@app.get("/health", response_model=HealthCheck)
async def health_check() -> HealthCheck:
    """Health check endpoint."""
    return HealthCheck(vector_store_ready=vector_store.is_ready())


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """Analyze code patterns."""
    try:
        similarity, matches = analyze_code(request.code, request.pattern)
        return AnalyzeResponse(similarity=similarity, matches=matches)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/encode")
async def encode(text: str) -> dict:
    """Encode text to vector."""
    try:
        return {"vector": encode_text(text).tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
