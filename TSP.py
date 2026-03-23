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

def create_random_population(cities : list[City], size : int):
    pop = []
    for _ in range(size):
        pop.append(create_sample_random(cities))
    # print(f"New population created : {pop}")
    return pop

def create_sample_random(cities : list[City]):
    sample = cities
    shuffled = random.sample(sample, len(sample))
    # print(f"sample created : {shuffled}")
    return shuffled

def evaluate_population(population : list[list[City]]):
    result : list[tuple[float, list[City]]] = []
    for sample in population:
        elem : tuple[float, list[City]]
        coords = extract_coords(sample)
        score = eval_dist(coords)
        elem = (score, sample)
        result.append(elem)
    return result

def roulette_select_population(evaluated_population: list[tuple[float, list[City]]], size):
    """
    evaluated_population: list of (distance, path)
    returns: one (distance, path) selected via roulette
    """

    if size > len(evaluated_population):
        raise ValueError("Size > pop size")
    # Convert distances to weights (smaller distance = higher weight)
    epsilon = 1e-9  # avoid division by zero
    weights = [1 / (dist + epsilon) for dist, _ in evaluated_population]

    total = sum(weights)

    new_pop = []
    for i in range(size):
        r = random.uniform(0, total)
        cumulative = 0.0
        for (dist, path), w in zip(evaluated_population, weights):
            cumulative += w
            if r <= cumulative:
                new_pop.append(path)
                break
    return new_pop

def mutation_swap(individu: list[City]) -> list[City]:
    mutant = individu[:]
    i, j = random.sample(range(len(mutant)), 2)
    mutant[i], mutant[j] = mutant[j], mutant[i]
    return mutant


def mutation_inversion(individu: list[City]) -> list[City]:
    mutant = individu[:]
    i, j = sorted(random.sample(range(len(mutant)), 2))
    mutant[i:j + 1] = reversed(mutant[i:j + 1])
    return mutant


def mutation_insertion(individu: list[City]) -> list[City]:
    mutant = individu[:]
    i, j = random.sample(range(len(mutant)), 2)
    ville = mutant.pop(i)
    mutant.insert(j, ville)
    return mutant


def mutation(
    population: list[list[City]],
    size_new_pop: int,
    taux_mutation: float = 0.5,
    type_mutation: str = "swap",
) -> list[list[City]]:
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

def solve_tsp(cities: list[City], size_pop: int, iterations: int):

    pop = create_random_population(cities, size_pop)
    eval_pop = evaluate_population(pop)

    for i in range(iterations):
        selected = roulette_select_population(eval_pop, size_pop // 2)

        pop = mutation(selected, size_pop, )

        eval_pop = evaluate_population(pop)

    min = np.inf
    result = []

    for sample in eval_pop:
        if sample[0] < min:
            min = sample[0]
            result = sample[1]

    return result


def solve_TSP_threaded(thread_id, cities):
    path = solve_tsp(cities, POP_SIZE, ITER)
    score = eval_dist(extract_coords(path))
    # print(f"Result from thread {thread_id} : {score}")
    return score, path