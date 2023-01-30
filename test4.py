import random
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import deap

def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def evaluate(individual, n_planes, capacity, origin, destinations):
    distances = [euclidean_distance(origin, destinations[i]) for i in individual]
    distances.sort() # sort the distances in ascending order
    reach = 0
    for i in range(len(distances)):
        if reach + 2 * distances[i] <= capacity * n_planes:
            reach += 2 * distances[i]
            n_planes -= 1
        else:
            break
    return reach / (2 * capacity),

def genetic_algorithm(n_planes, capacity, origin, destinations):
    # Define the GA
    creator.create("FitnessMax", deap.base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    
    toolbox = deap.base.Toolbox()
    toolbox.register("indices", random.sample, range(len(destinations)), len(destinations))
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate, n_planes=n_planes, capacity=capacity, origin=origin, destinations=destinations)
    toolbox.register("mate", deap.tools.cxPartialyMatched)
    toolbox.register("mutate", deap.tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", deap.tools.selTournament, tournsize=3)
    
    pop = toolbox.population(n=100)
    hof = deap.tools.HallOfFame(1)
    stats = deap.tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)
    
    pop, log = deap.algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=50, stats=stats, halloffame=hof)
    
    best_individual = hof[0]
    return int(evaluate(best_individual, n_planes, capacity, origin, destinations)[0]), best_individual

# Example usage
n_planes = 5
capacity = 6
origin = (0, 0)
destinations = [(100, 100), (200, 200), (300, 300)]

number_of_destinations, best_individual = genetic_algorithm(n_planes, capacity, origin, destinations)
print(number_of_destinations, best_individual)