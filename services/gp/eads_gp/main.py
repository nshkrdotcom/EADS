"""GP service FastAPI application."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from gp_engine.gp_service import evolve_solution

app = FastAPI(title="EADS GP Service")


class HealthCheck(BaseModel):
    """Health check response model for the GP service.

    Attributes:
        status (str): The current status of the service
        service (str): The name of the service
        gpu_available (bool): Whether GPU acceleration is available
    """

    status: str = "healthy"
    service: str = "gp"
    gpu_available: bool = True


class EvolveRequest(BaseModel):
    """Request model for evolving solutions using genetic programming.

    Attributes:
        code (str): Initial code solution
        fitness_function (str): The fitness function to evaluate solutions
        population_size (int): Size of the population
        generations (int): Number of generations to evolve
    """

    code: str
    fitness_function: str
    population_size: int = 100
    generations: int = 50


class Solution(BaseModel):
    """Model representing an evolved solution.

    Attributes:
        code (str): The evolved code solution
        fitness (float): The fitness score of the solution
        generation (int): Generation number of the solution
    """

    code: str
    fitness: float
    generation: int


@app.get("/health", response_model=HealthCheck)
async def health_check() -> HealthCheck:
    """Health check endpoint."""
    try:
        import torch

        gpu_available = torch.cuda.is_available()
    except ImportError:
        gpu_available = False
    return HealthCheck(gpu_available=gpu_available)


@app.post("/evolve", response_model=Solution)
async def evolve(request: EvolveRequest) -> Solution:
    """Evolve a solution using genetic programming."""
    try:
        code, fitness, generation = evolve_solution(
            request.code,
            request.fitness_function,
            request.population_size,
            request.generations,
        )
        return Solution(code=code, fitness=fitness, generation=generation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
