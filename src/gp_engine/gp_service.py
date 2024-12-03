"""Genetic Programming Service for code evolution."""

import logging
import logging.config
from typing import Any, Dict, List

import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from src.config.settings import GP_CONFIG, LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

app: FastAPI = FastAPI(
    title="GP Service",
    description="A service for genetic programming optimization",
    version="1.0.0",
)


class Individual:
    """Individual in the genetic programming population."""

    def __init__(self, code: str, fitness: float = 0.0):
        """Initialize individual.

        Args:
            code: Code representation
            fitness: Fitness score
        """
        self.code = code
        self.fitness = fitness


class GPInput(BaseModel):
    """Input model for GP operations."""

    code: str
    population_size: int = Field(default=GP_CONFIG["population_size"], gt=0)
    generations: int = Field(default=GP_CONFIG["generations"], gt=0)
    mutation_rate: float = Field(default=GP_CONFIG["mutation_rate"], ge=0.0, le=1.0)
    crossover_rate: float = Field(default=GP_CONFIG["crossover_rate"], ge=0.0, le=1.0)
    encoding: List[float] = []


def evaluate_fitness(individual: Individual) -> float:
    """Evaluate fitness of an individual.

    Args:
        individual: Individual to evaluate

    Returns:
        float: Fitness score
    """
    # Placeholder: return a random fitness score
    return 0.95


def initialize_population(code: str, size: int) -> List[Individual]:
    """Initialize population for genetic programming.

    Args:
        code: Initial code to base population on
        size: Size of population to initialize

    Returns:
        List[Individual]: Initialized population
    """
    return [Individual(code=code) for _ in range(size)]


@app.get("/", response_model=Dict[str, str])
async def read_root() -> Dict[str, str]:
    """Root endpoint.

    Returns:
        Dict[str, str]: Service status message
    """
    return {"message": "GP Service is running"}


@app.post("/evolve", response_model=Dict[str, Any])
async def evolve_solution(input_data: GPInput) -> Dict[str, Any]:
    """Evolve solution using genetic programming.

    Args:
        input_data: Input parameters for evolution

    Returns:
        Dict[str, Any]: Evolution results

    Raises:
        HTTPException: If evolution fails
    """
    try:
        # Initialize population
        population = initialize_population(input_data.code, input_data.population_size)

        # Evaluate initial population
        for individual in population:
            individual.fitness = evaluate_fitness(individual)

        # Find best individual
        best_individual = max(population, key=lambda x: x.fitness)

        return {
            "best_individual": best_individual.code,
            "fitness": best_individual.fitness,
        }
    except Exception as e:
        logger.error(f"Error in GP evolution: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@app.exception_handler(Exception)
async def exception_handler(request: Any, exc: Exception) -> JSONResponse:
    """Handle general exceptions.

    Args:
        request: FastAPI request
        exc: Exception that was raised

    Returns:
        JSONResponse: Error response
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": "error", "message": str(exc)},
    )


if __name__ == "__main__":
    uvicorn.run(
        "src.gp_engine.gp_service:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
    )
