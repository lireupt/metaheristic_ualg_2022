import random
import numpy as np

def generate_random_individual(destinations, demand, capacity, n_planes):
    individual = []
    for i in range(len(destinations)):
        individual.append([random.randint(0, n_planes-1) for j in range(demand[i])])
    return individual

def calc_fitness(individual, destinations, demand, capacity, n_planes):
    plane_capacity = [capacity for i in range(n_planes)]
    for i in range(len(destinations)):
        for j in range(demand[i]):
            plane_capacity[individual[i][j]] -= 1
            if plane_capacity[individual[i][j]] < 0:
                return 0
    return 1

def crossover_individual(individual1, individual2, dest, demand, cap, planes):
    ind1 = individual1.copy()
    ind2 = individual2.copy()
    for i in range(len(dest)):
        for j in range(demand[i]):
            if random.uniform(0, 1) < 0.5:
                ind1[i][j], ind2[i][j] = ind2[i][j], ind1[i][j]
    return ind1, ind2

def mutation_individual(individual, dest, demand, cap, planes):
    for i in range(len(dest)):
        for j in range(demand[i]):
            if random.uniform(0, 1) < 0.1:
                individual[i][j] = random.randint(0, planes-1)
    return individual

def genetic_algorithm(destinations, demand, capacity, n_planes, pop_size=100, n_generations=100):
    population = [generate_random_individual(destinations, demand, capacity, n_planes) for i in range(pop_size)]
    for generation in range(n_generations):
        fitness = [calc_fitness(individual, destinations, demand, capacity, n_planes) for individual in population]
        population = [x for _, x in sorted(zip(fitness, population), reverse=True)]
        population = population[:int(0.2*pop_size)]
        while len(population) < pop_size:
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            child1, child2 = crossover_individual(parent1, parent2, destinations, demand, capacity, n_planes)
            child1 = mutation_individual(child1, destinations, demand, capacity, n_planes)
            child2 = mutation_individual(child2, destinations, demand, capacity, n_planes)
            population.append(child1)
            population.append(child2)
    return population[0]

n_planes = 5
capacity = 6
origin = (0, 0)
destinations = [(100, 100), (200, 200), (300, 300)]
demand = [4, 5, 6]

result = genetic_algorithm(destinations, demand, capacity, n_planes, pop_size=100, n_generations=100)
print (result)