import random
import numpy as np
import matplotlib.pyplot as plt
import csv

#Simular um ataque aos pontos azuis definimos o numero de avioes e a capacidade de transporte de armas 
# para simular em quanto tempo precisamos para fazer o maior numero de estragos e todos os pontos.
#função de avalição

# Problem parameters
n_planes = 15
capacity = 6
origin = (37.19288993230424, -8.43550218806426)
destinations = [(37.46319, -8.23729),(37.783355, -8.64717),(38.61811, -8.29787)]


# destinations = [(37.463194207680495, -8.237291771914505),
#                 (37.783354090148315, -8.647170654187905),
#                 (38.61811210448749, -8.297872443397525),
#                 (38.25897372829287, -8.589068891749571),
#                 (40.506360363856096, -5.2531535147774635),
#                 (43.28542466147749, -3.4873874430162215),
#                 (43.61434387783453, 3.75417109005078)]


n_destinations = len(destinations)
# demand = [4, 5, 6]


# Distance function
def distance(a, b):
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# Fitness function
def fitness(individual, distances):
    reach = 0
    for plane in range(n_planes):
        start = origin
        plane_capacity = capacity
        for i in individual:
            if plane_capacity == 0:
                break
            elif i < n_destinations and distances[start][destinations[i]] <= plane_capacity:
                reach += 1
                plane_capacity -= distances[start][destinations[i]]
                start = destinations[i]
    return reach

# Genetic algorithm
def genetic_algorithm(distances):
    pop_size = 100
    n_generations = 1000
    mutation_prob = 0.05
    best_reach = 0
    best_individual = None

    population = [np.random.permutation(n_destinations) for i in range(pop_size)]
    for generation in range(n_generations):
        fits = [fitness(individual, distances) for individual in population]
        best_fit = max(fits)
        if best_fit > best_reach:
            best_reach = best_fit
            best_individual = population[fits.index(best_fit)]
        parents = [population[fits.index(f)] for f in sorted(fits, reverse=True)[:pop_size//2]]
        offspring = [np.random.permutation(n_destinations) for i in range(pop_size - len(parents))]
        for i in range(len(parents)):
            for j in range(len(parents)):
                if i != j:
                    offspring.append(np.concatenate((parents[i][:n_destinations//2], parents[j][n_destinations//2:])))
        for i in range(len(offspring)):
            if random.uniform(0, 1) < mutation_prob:
                offspring[i][random.randint(0, n_destinations-1)], offspring[i][random.randint(0, n_destinations-1)] = offspring[i][random.randint(0, n_destinations-1)], offspring[i][random.randint(0, n_destinations-1)]
        population = parents + offspring

    return best_reach, best_individual

# Plotting function
# def plot_solution(individual, distances, reach):
#     fig, ax = plt.subplots()
#     ax.scatter(*zip(*destinations), color='red')
#     ax.scatter(*origin, color='blue')
#     ax.annotate(f'{reach} deliveries', (50, 50), fontsize=12)
#     for i in individual:
#         if i < len(destinations):
#             ax.plot(*zip(destinations[i], destinations[i-1]), 'k-', lw=1)
#     plt.show()


# Plot function
# def plot_destinations(origin, destinations, individual, distances):
#     x = [origin[0]] + [i[0] for i in destinations]
#     y = [origin[1]] + [i[1] for i in destinations]
#     plt.scatter(x, y)
#     start = origin
#     for i in individual:
#         if i < n_destinations:
#             x_line = [start[0], destinations[i][0]]
#             y_line = [start[1], destinations[i][1]]
#             plt.plot(x_line, y_line, 'b-')
#             start = destinations[i]
#     plt.show()

def plot_destinations(origin, destinations, individual, distances, capacity):
    plt.scatter([origin[0]], [origin[1]], c='red', label='Starting Point')
    x = [i[0] for i in destinations]
    y = [i[1] for i in destinations]
    plt.scatter(x, y)
    start = origin
    capacities = [capacity for i in range(n_destinations)]
    for i in individual:
        if i < n_destinations:
            color = 'green' if capacities[i] > 0 else 'red'
            x_line = [start[0], destinations[i][0]]
            y_line = [start[1], destinations[i][1]]
            plt.plot(x_line, y_line, color)
            if capacities[i] == 0:
                end = origin
                capacities[i] = capacity
            else:
                end = destinations[i]
                capacities[i] -= 1
            start = end
    plt.show()


# Time calculation function
def time_to_reach(individual, distances):
    times = [0] * n_destinations
    n_reaches = [1 for i in range(n_destinations)] # number of reaches required for each destination
    plane_capacity = capacity
    start = origin
    for i in individual:
        if plane_capacity == 0:
            plane_capacity = capacity
            start = origin
            break
        elif i < n_destinations:
            if n_reaches[i] > 0:
                if times[i] == 0:
                    times[i] = distances[start][destinations[i]]
                else:
                    times[i] = min(times[i], distances[start][destinations[i]])
                n_reaches[i] -= 1
                plane_capacity -= distances[start][destinations[i]]
                start = destinations[i]
    return times



# def time_to_reach(p1, p2, capacity, demand, n_planes):
#     total_time = 0
#     current_capacity = 0
#     origin = (0, 0)
#     for i in range(n_planes):
#         total_time += distance(p1, p2)
#         current_capacity += demand
#         if current_capacity >= capacity:
#             current_capacity = 0
#             total_time += 2 * distance(p2, origin)
#             p1 = origin
#     return total_time



# Main
distances = {dest: {dest2: distance(dest, dest2) for dest2 in destinations + [origin]} for dest in destinations + [origin]}
reach, individual = genetic_algorithm(distances)
print("Reach:", reach)
print("Individual:", individual)


#Time
times = time_to_reach(individual, distances)
capacities = [capacity for i in range(n_destinations)]
print("Times to reach each destination:", times)
plot_destinations(origin, destinations, individual, distances, capacity)





# times = time_to_reach(individual, distances)
# print("Times to reach each destination:", times)

# Write to CSV file
# with open('destination_times.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(["Destination", "Time"])
#     for i, time in enumerate(times):
#         writer.writerow([destinations[i], time])

# Plot
# plot_solution(individual, distances, reach)
# plot_destinations(origin, destinations, individual, distances)