"""Genetic Programming Service for code evolution."""

import logging
import logging.config
import random
from typing import Any, Dict, List, Tuple

import deap.base
import deap.creator
import deap.tools
import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from src.config.settings import GP_CONFIG, LOGGING_CONFIG
from src.error_handling.error_handler import ModelError

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

app: FastAPI = FastAPI(
    title="GP Service",
    description="A service for genetic programming optimization",
    version="1.0.0",
)

# Create types for genetic programming
deap.creator.create("FitnessMax", deap.base.Fitness, weights=(1.0,))
deap.creator.create("Individual", list, fitness=deap.creator.FitnessMax)

# Initialize toolbox
toolbox = deap.base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register(
    "individual",
    deap.tools.initRepeat,
    deap.creator.Individual,
    toolbox.attr_bool,
    n=100,
)
toolbox.register("population", deap.tools.initRepeat, list, toolbox.individual)


class GPInput(BaseModel):
    """Input model for GP operations."""

    code: str
    population_size: int = Field(default=GP_CONFIG["population_size"], gt=0)
    generations: int = Field(default=GP_CONFIG["generations"], gt=0)
    mutation_rate: float = Field(default=GP_CONFIG["mutation_rate"], ge=0.0, le=1.0)
    crossover_rate: float = Field(default=GP_CONFIG["crossover_rate"], ge=0.0, le=1.0)


def evaluate_fitness(individual: List[Any]) -> Tuple[float]:
    """Evaluate fitness of an individual.

    Args:
        individual: Individual to evaluate

    Returns:
        Tuple[float]: Fitness score
    """
    return (sum(individual),)


def initialize_population(population_size: int) -> List[Any]:
    """Initialize population for genetic programming.

    Args:
        population_size: Size of population to initialize

    Returns:
        List[Any]: Initialized population
    """
    return [[] for _ in range(population_size)]


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
        population = initialize_population(input_data.population_size)

        # Set up genetic operators
        toolbox.register("evaluate", evaluate_fitness)
        toolbox.register("mate", deap.tools.cxTwoPoint)
        toolbox.register("mutate", deap.tools.mutFlipBit, indpb=0.05)
        toolbox.register("select", deap.tools.selTournament, tournsize=3)

        # Evaluate initial population
        fitnesses = list(map(toolbox.evaluate, population))
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit

        # Evolution loop
        for gen in range(input_data.generations):
            # Select next generation
            offspring = toolbox.select(population, len(population))
            offspring = list(map(toolbox.clone, offspring))

            # Apply crossover
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < input_data.crossover_rate:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            # Apply mutation
            for mutant in offspring:
                if random.random() < input_data.mutation_rate:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

            # Evaluate invalid individuals
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = list(map(toolbox.evaluate, invalid_ind))
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # Replace population
            population[:] = offspring

            best_fitness = max(ind.fitness.values[0] for ind in population)
            logger.info(f"Generation {gen}: Best fitness = {best_fitness}")

        # Get best solution
        best_ind = max(population, key=lambda x: x.fitness.values[0])

        return {
            "best_individual": list(best_ind),
            "fitness": best_ind.fitness.values[0],
        }
    except Exception as e:
        logger.error(f"Error in GP evolution: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@app.exception_handler(ModelError)
async def model_error_handler(request: Any, exc: ModelError) -> JSONResponse:
    """Handle model errors.

    Args:
        request: FastAPI request
        exc: Model error exception

    Returns:
        JSONResponse: Error response
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"status": "error", "message": str(exc)},
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
