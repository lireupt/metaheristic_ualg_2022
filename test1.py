from scipy.optimize import linprog

def optimize_destinations(planes, supplies, capacities, costs):
    c = [-1 for i in range(len(capacities))]
    b = [supplies]
    bounds = [(0, float('inf')) for i in range(len(capacities))]
    res = linprog(c, A_ub=capacities, b_ub=b, bounds=bounds, method='simplex')
    return res.fun

# Example usage
planes = 5
supplies = 10
capacities = [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]
costs = [-1, -1, -1, -1, -1]

print("Number of destinations reached:", -optimize_destinations(planes, supplies, capacities, costs))
