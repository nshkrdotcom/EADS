"""GP service FastAPI application."""
from eads_core.logging import ServiceLogger, log_operation
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from .gp_engine.gp_service import evolve_solution

app = FastAPI(title="EADS GP Service")
logger = ServiceLogger("gp")

# Log service startup
logger.log_startup(
    {"service": "gp", "gpu_available": True}  # TODO: Actually check GPU availability
)


class HealthCheck(BaseModel):
    """Health check response model for the GP service."""

    status: str = "healthy"
    service: str = "gp"
    gpu_available: bool = True


class EvolveRequest(BaseModel):
    """Request model for evolving solutions using genetic programming."""

    code: str
    fitness_function: str
    population_size: int = 100
    generations: int = 50


class Solution(BaseModel):
    """Model representing an evolved solution."""

    code: str
    fitness: float
    generation: int


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
        # TODO: Actually check GPU availability
        gpu_available = True
        ctx.update(gpu_available=gpu_available)
        return HealthCheck(gpu_available=gpu_available)


@app.post("/evolve", response_model=Solution)
async def evolve(request: EvolveRequest) -> Solution:
    """Evolve a solution using genetic programming."""
    with log_operation(
        "evolve_solution",
        code_length=len(request.code),
        fitness_func_length=len(request.fitness_function),
        population_size=request.population_size,
        generations=request.generations,
    ) as ctx:
        try:
            code, fitness, generation = evolve_solution(
                request.code,
                request.fitness_function,
                request.population_size,
                request.generations,
            )
            ctx.update(final_fitness=fitness, final_generation=generation)
            return Solution(code=code, fitness=fitness, generation=generation)
        except Exception as e:
            ctx.update(error=str(e))
            raise HTTPException(status_code=500, detail=str(e))
