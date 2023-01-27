import random
import pandas as pd

def heuristic_function(hits, misses, effective_shots, total_shots):
    if effective_shots == 0:
        return -1
    hit_rate = hits / effective_shots
    miss_rate = misses / total_shots
    return (hit_rate * 0.7) + (miss_rate * -0.3)

def create_chromosome():
    chromosome = []
    for i in range(10):
        gene = random.randint(0, 1)
        chromosome.append(gene)
    return chromosome

def initialize_population(population_size):
    population = []
    for i in range(population_size):
        chromosome = create_chromosome()
        population.append(chromosome)
    return population

def crossover(chromosome1, chromosome2):
    crossover_point = random.randint(1, len(chromosome1) - 1)
    new_chromosome = chromosome1[:crossover_point] + chromosome2[crossover_point:]
    return new_chromosome

def mutate(chromosome):
    mutation_point = random.randint(0, len(chromosome) - 1)
    chromosome[mutation_point] = random.randint(0, 1)
    return chromosome

def select_survivors(population, fitness_function):
    population_fitness = []
    for chromosome in population:
        hits = random.randint(0, 100)
        misses = random.randint(0, 100)
        effective_shots = random.randint(0, 100)
        total_shots = random.randint(0, 100)
        fitness = fitness_function(hits, misses, effective_shots, total_shots)
        if fitness < 0:
            continue
    population_fitness.append((chromosome, fitness))
    population_fitness.sort(key=lambda x: x[1], reverse=True)
    return population_fitness[:int(len(population_fitness) / 2)]

results_table = pd.DataFrame(columns=['Geração', 'Melhor aptidão', 'Pior aptidão', 'Média aptidão'])

population_size = 100
max_generations = 100

population = initialize_population(population_size)

for generation in range(max_generations):
    survivors = select_survivors(population, heuristic_function)
    new_population = []
while len(new_population) < population_size:
    parent1 = random.choice(survivors)[0]
    parent2 = random.choice(survivors)[0]
    child = crossover(parent1, parent2)
    child = mutate(child)
    new_population.append(child)
    population = new_population
# calcula as estatísticas de aptidão da geração
generation_fitness = [fitness for _, fitness in select_survivors(population, heuristic_function)]
best_fitness = max(generation_fitness)
worst_fitness = min(generation_fitness)
avg_fitness = sum(generation_fitness) / len(generation_fitness)
results_table = results_table.append({
'Geração': generation,
'Melhor aptidão': best_fitness,
'Pior aptidão': worst_fitness,
'Média aptidão': avg_fitness
}, ignore_index=True)

print(results_table)
