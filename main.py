import numpy as np
import sys
from tqdm import tqdm
from itertools import permutations

# Reading CSV-file input
def parse_input (filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    cities = []
    distances = []

    for line in lines:
            values = line.strip().split(',')
            city = values[0] # first element is a city name
            cities.append(city)
            distance = list(map(int, values[1:])) # next elements are a row of distance map
            distances.append(distance)

    return cities, np.array(distances)

# Calculating fitness
def calculate_fitness (route, distances):
    distance = 0
    for i in range(len(route) - 1):
        distance += distances[route[i]][route[i + 1]]
    distance += distances[route[-1]][route[0]]
    return distance

# Bruteforce algorithm
def bruteforce(cities, distances):
    best_tour = None
    best_distance = float('inf')

    for perm in permutations(range(len(cities))):
        current_distance = calculate_fitness(list(perm), distances)
        if current_distance < best_distance:
            best_distance = current_distance
            best_tour = list(perm)

    return best_tour

# Initialize tour by choosing random neighbors
def initialize_tour (paths):
    num_cities = paths.shape[0]
    visited = [False] * num_cities

    tour = [np.random.randint(0, num_cities)]
    visited[tour[0]] = True

    while len(tour) < num_cities:
        current_city = tour[-1]
        nearest_city = None
        nearest_distance = float('inf')

        for city in range(num_cities):
            if not visited[city] and paths[current_city, city] < nearest_distance:
                nearest_city = city
                nearest_distance = paths[current_city, city]

        tour.append(nearest_city)
        visited[nearest_city] = True

    return tour


def get_neighbors (x, n = 20):
    neighbors = []

    while len(neighbors) < n:
        i = np.random.randint(0, len(x) - 2)
        j = np.random.randint(1, len(x) - 1)
        if i > j:
            i, j = j, i # make sure j is always bigger
        neighbor = x.copy()
        neighbor[i:j] = neighbor[i:j][::-1] #reverse i:j part of list
        if tuple(neighbor) not in map(tuple, neighbors):
            neighbors.append(neighbor)

    return neighbors

def best_neighbor (
        x: list,
        paths: np.array,
        get_neighbors: callable = get_neighbors,
        fitness_func: callable = calculate_fitness):
    neighbors = get_neighbors(x)
    best_neighbor = neighbors[0]
    for neighbor in neighbors:
        if fitness_func(neighbor, paths) < fitness_func(best_neighbor, paths):
            best_neighbor = neighbor
    return best_neighbor

def random_neighbor (
        x: list,
        get_neighbors: callable = get_neighbors):
    neighbors = get_neighbors(x)
    return neighbors[np.random.randint(0, len(neighbors))]

def hill_climbing (
        f: callable,
        x_init: list,
        n_iters: int,
        paths: np.array,
        variant: str,
        steepest: bool = False):
    x = x_init
    x_best = x_init

    neighbor_function = best_neighbor if variant == 'simple' else random_neighbor

    for iteration in tqdm(range(n_iters)):
        y = neighbor_function(x, paths)
        if f(y, paths) < f(x, paths):
            x = y
            if f(x, paths) < f(x_best, paths):
                x_best = x
            else:
                if steepest:
                    x = x_best

    return x_best

# Function to print tour
def print_result(tour, cities, distances):
    total_distance = 0
    for i in range(len(tour) - 1):
        city_from = cities[tour[i]]
        city_to = cities[tour[i + 1]]
        distance = distances[tour[i], tour[i + 1]]
        print(f"{city_from} -> {city_to}: {distance} km")
        total_distance += distance
    distance = distances[tour[-1], tour[0]]
    print(f"{cities[tour[-1]]} -> {cities[tour[0]]}: {distance} km")
    total_distance += distance
    print(f"Total distance: {total_distance} km\n")

def main ():
    filename = sys.argv[1]
    algorithm = sys.argv[2]
    cities, distances = parse_input(filename)
    initial_tour = initialize_tour(distances)
    print("Initial tour:")
    print_result(initial_tour, cities, distances)

    if algorithm == 'hill-climbing':
        best_tour = hill_climbing(
            f = calculate_fitness,
            x_init=initial_tour,
            n_iters=1000,
            paths=distances,
            variant='simple',
            steepest=True
        )
        print("Best tour:")
        print_result(best_tour, cities, distances)
    elif algorithm == 'bruteforce':
        best_tour = bruteforce(cities, distances)
        print_result(best_tour, cities, distances)


if __name__ == '__main__':
    main()