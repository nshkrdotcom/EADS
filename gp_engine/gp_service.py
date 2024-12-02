import os
import random

import numpy as np
import uvicorn
from deap import algorithms, base, creator, tools
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from neo4j import GraphDatabase

load_dotenv()

app = FastAPI()

# Neo4j connection
neo4j_uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
neo4j_user = os.getenv("NEO4J_USER", "neo4j")
neo4j_password = os.getenv("NEO4J_PASSWORD", "password")

neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

# Initialize DEAP
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()


@app.get("/")
def read_root():
    return {"status": "GP Engine is running"}


@app.post("/evolve")
async def evolve_code(code: str, generations: int = 10):
    try:
        # Initialize population
        population = toolbox.population(n=50)

        # Evolve
        for gen in range(generations):
            offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)
            fits = toolbox.map(toolbox.evaluate, offspring)
            for fit, ind in zip(fits, offspring):
                ind.fitness.values = fit
            population = toolbox.select(offspring, k=len(population))

        return {
            "status": "success",
            "generations": generations,
            "best_fitness": max([ind.fitness.values[0] for ind in population]),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
