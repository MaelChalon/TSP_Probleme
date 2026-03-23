import random

from clientHTTP.ClientHTTP import ClientHTTP
from tools import *


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
    print(f"New population created : {pop}")
    return pop

def create_sample_random(cities : list[City]):
    sample = cities
    shuffled = random.sample(sample, len(sample))
    print(f"sample created : {shuffled}")
    return shuffled

def evaluate_population(population : list[list[City]]):
    result : list[tuple[float, list[City]]] = []
    for sample in population:
        elem : tuple[float, list[City]]
        score = eval_dist(sample)
        elem = (score, sample)
        result.append(elem)
    return result

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
    taux_mutation: float = 0.8,
    type_mutation: str = "inversion",
) -> list[list[City]]:
    if not population:
        return []
    nouvelle_population = [ind[:] for ind in population]

    while len(nouvelle_population) < len(population):
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


