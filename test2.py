import random
import math
import matplotlib.pyplot as plt

# Constants
n_planes = 5
capacity = 6
origin = (0, 0)
destinations = [(100, 100), (200, 200), (300, 300)]

def distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def calculate_cost(route):
    total_distance = 0
    for i in range(0, len(route), 2):
        total_distance += distance(route[i], route[i+1])
    return total_distance

def generate_initial_solution():
    route = []
    for i in range(n_planes):
        route.append(origin)
        route.append(random.choice(destinations))
    return route

def make_random_move(route):
    i = random.randint(0, len(route) - 1)
    j = random.randint(0, len(route) - 1)
    route[i], route[j] = route[j], route[i]
    return route

def simulated_annealing(route, T):
    while T > 1e-3:
        new_route = make_random_move(route)
        delta = calculate_cost(new_route) - calculate_cost(route)
        if delta < 0:
            route = new_route
        else:
            p = math.exp(-delta / T)
            if random.uniform(0, 1) < p:
                route = new_route
        T *= 0.995
    return route

def plot_solution(route):
    x = [coord[0] for coord in route]
    y = [coord[1] for coord in route]
    plt.plot(x, y, '-o')
    for coord in destinations:
        plt.scatter(coord[0], coord[1], color='red')
        plt.scatter(origin[0], origin[1], color='blue')
        plt.title("Airplane Routing Optimization Solution")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.show()

def main():
    route = generate_initial_solution()
    final_route = simulated_annealing(route, 1000)
    print("Final route:", final_route)
    print("Total cost:", calculate_cost(final_route))
    plot_solution(final_route)

if __name__ == '__main__':
    main()


    origin = (21.962100281510644, -157.97050724922886)
destinations = [(21.362371733736136, -157.9603367767048)]
