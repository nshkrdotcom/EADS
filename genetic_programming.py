from deap import base, creator, tools, algorithms
import random

def run_genetic_programming():
    print("Running genetic programming cycle...")
    
    # Define the problem domain
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    
    toolbox = base.Toolbox()
    toolbox.register("attr_float", random.random)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, 10)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    def eval_function(individual):
        return sum(individual),
    
    toolbox.register("evaluate", eval_function)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)
    
    population = toolbox.population(n=300)
    algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=40, verbose=True)
    
    print("Genetic programming cycle completed.")
