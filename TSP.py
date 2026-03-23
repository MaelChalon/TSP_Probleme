import random
import numpy as np
from tools import *

POP_SIZE = 100
ITER = 1000

class City:
    id: int
    coord: tuple[float, float]

    def __init__(self, id, coord: tuple[float, float]):
        self.id = id
        self.coord = coord

    def __repr__(self):
        return f"City(id={self.id}, coord={self.coord})"

# Generate a population of random city sequences
def create_random_population(cities: list[City], size: int):
    pop = [create_sample_random(cities) for _ in range(size)]
    return pop

# Create a single random permutation of cities
def create_sample_random(cities: list[City]):
    return random.sample(cities, len(cities))

# Evaluate all individuals by calculating total path distance
def evaluate_population(population: list[list[City]]):
    result = []
    for sample in population:
        coords = extract_coords(sample)
        score = eval_dist(coords)
        result.append((score, sample))
    return result

# Roulette-wheel selection: prefer shorter distances
def roulette_select_population(evaluated_population: list[tuple[float, list[City]]], size):
    if size > len(evaluated_population):
        raise ValueError("Size > pop size")
    epsilon = 1e-9
    weights = [1 / (dist + epsilon) for dist, _ in evaluated_population]
    total = sum(weights)

    new_pop = []
    for _ in range(size):
        r = random.uniform(0, total)
        cumulative = 0.0
        for (dist, path), w in zip(evaluated_population, weights):
            cumulative += w
            if r <= cumulative:
                new_pop.append(path)
                break
    return new_pop

# Tournament selection: pick the best individual from random subsets
def tournament_select_population(evaluated_population: list[tuple[float, list[City]]], size, tournament_size=3):
    if size > len(evaluated_population):
        raise ValueError("Size > pop size")
    
    new_pop = []
    for _ in range(size):
        # Pick random competitors
        competitors = random.sample(evaluated_population, tournament_size)
        # Select the one with smallest distance
        winner = min(competitors, key=lambda x: x[0])
        new_pop.append(winner[1])
    
    return new_pop

# Swap two cities in a path
def mutation_swap(individu: list[City]) -> list[City]:
    mutant = individu[:]
    i, j = random.sample(range(len(mutant)), 2)
    mutant[i], mutant[j] = mutant[j], mutant[i]
    return mutant

# Reverse a sub-path
def mutation_inversion(individu: list[City]) -> list[City]:
    mutant = individu[:]
    i, j = sorted(random.sample(range(len(mutant)), 2))
    mutant[i:j + 1] = reversed(mutant[i:j + 1])
    return mutant

# Remove a city and insert it elsewhere
def mutation_insertion(individu: list[City]) -> list[City]:
    mutant = individu[:]
    i, j = random.sample(range(len(mutant)), 2)
    ville = mutant.pop(i)
    mutant.insert(j, ville)
    return mutant

# Apply chosen mutation to population until new size is reached
def mutation(population: list[list[City]], size_new_pop: int, taux_mutation: float = 0.5, type_mutation: str = "swap") -> list[list[City]]:
    if not population:
        return []
    nouvelle_population = [ind[:] for ind in population]

    while len(nouvelle_population) < size_new_pop:
        parent = random.choice(population)
        enfant = parent[:]
        if random.random() < taux_mutation:
            if type_mutation == "swap":
                enfant = mutation_swap(enfant)
            elif type_mutation == "inversion":
                enfant = mutation_inversion(enfant)
            elif type_mutation == "insertion":
                enfant = mutation_insertion(enfant)
            else:
                raise ValueError("Type de mutation inconnu")
        nouvelle_population.append(enfant)

    return nouvelle_population

# Main TSP solver using genetic algorithm
def solve_tsp(cities: list[City], size_pop: int, iterations: int):
    pop = create_random_population(cities, size_pop)
    eval_pop = evaluate_population(pop)

    for _ in range(iterations):
        selected = roulette_select_population(eval_pop, size_pop // 2)
        pop = mutation(selected, size_pop)
        eval_pop = evaluate_population(pop)

    # Return the best path
    min_dist = np.inf
    result = []
    for score, path in eval_pop:
        if score < min_dist:
            min_dist = score
            result = path
    return result

# Threaded wrapper for TSP solver
def solve_TSP_threaded(thread_id, cities):
    path = solve_tsp(cities, POP_SIZE, ITER)
    score = eval_dist(extract_coords(path))
    return score, path