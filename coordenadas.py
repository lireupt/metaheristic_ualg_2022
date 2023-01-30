import numpy as np

np.random.seed(0) # for reproducibility

num_coordinates = 100
min_coordinate = 0
max_coordinate = 1000

random_coordinates = np.random.randint(min_coordinate, max_coordinate, (num_coordinates, 2))
print(random_coordinates)
