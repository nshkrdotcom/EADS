"""NLP service FastAPI application."""
from typing import List

from eads_core.logging import ServiceLogger, log_operation
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from .nlp.nlp_service import analyze_code, encode_text
from .vector_store import WeaviateClient, WeaviateConfig

app = FastAPI(title="EADS NLP Service")
logger = ServiceLogger("nlp")

# Initialize vector store
config = WeaviateConfig(host="localhost", port=8080)
vector_store = WeaviateClient(config)

# Log service startup
logger.log_startup(
    {"service": "nlp", "vector_store": {"host": config.host, "port": config.port}}
)


class HealthCheck(BaseModel):
    """Health check response model for the NLP service."""

    status: str = "healthy"
    service: str = "nlp"
    vector_store_ready: bool = True


class AnalyzeRequest(BaseModel):
    """Request model for code analysis."""

    code: str
    pattern: str


class AnalyzeResponse(BaseModel):
    """Response model for code analysis results."""

    similarity: float
    matches: List[str]


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests and responses."""
    ctx = logger.log_request(request.method, request.url.path)
    response = await call_next(request)
    logger.log_response(response.status_code, request_id=ctx.get("request_id"))
    return response


@app.get("/health", response_model=HealthCheck)
async def health_check() -> HealthCheck:
    """Health check endpoint."""
    with log_operation("health_check") as ctx:
        is_ready = vector_store.is_ready()
        ctx.update(vector_store_ready=is_ready)
        return HealthCheck(vector_store_ready=is_ready)


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """Analyze code patterns."""
    with log_operation(
        "analyze_code",
        code_length=len(request.code),
        pattern_length=len(request.pattern),
    ) as ctx:
        try:
            similarity, matches = analyze_code(request.code, request.pattern)
            ctx.update(similarity=similarity, num_matches=len(matches))
            return AnalyzeResponse(similarity=similarity, matches=matches)
        except Exception as e:
            ctx.update(error=str(e))
            raise HTTPException(status_code=500, detail=str(e))


@app.post("/encode")
async def encode(text: str) -> dict:
    """Encode text to vector."""
    with log_operation("encode_text", text_length=len(text)) as ctx:
        try:
            vector = encode_text(text).tolist()
            ctx.update(vector_length=len(vector))
            return {"vector": vector}
        except Exception as e:
            ctx.update(error=str(e))
            raise HTTPException(status_code=500, detail=str(e))
