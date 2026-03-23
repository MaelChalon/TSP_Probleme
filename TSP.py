import random
from tools import *

class City:
    id : int
    coord : tuple[float, float]
    
    def __init__(self, id, coord :tuple[float, float]):
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
        coords = [city.coord for city in sample]
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
        print(f"DBG {i}")
        r = random.uniform(0, total)
        cumulative = 0.0
        for (dist, path), w in zip(evaluated_population, weights):
            cumulative += w
            if r <= cumulative:
                new_pop.append((dist, path))
    return new_pop
                   

points = [
    City(1, (48.8566, 2.3522)),   # Paris
    City(2, (50.1109, 8.6821)),   # Frankfurt
    City(3, (52.5200, 13.4050)),  # Berlin
    City(4, (51.5074, -0.1278)),  # London
    City(5, (40.4168, -3.7038)),  # Madrid
    City(6, (41.9028, 12.4964)),  # Rome
    # City(7, (45.4642, 9.1900)),   # Milan
    # City(8, (52.3676, 4.9041)),   # Amsterdam
    # City(9, (50.8503, 4.3517)),   # Brussels
    # City(10, (48.2082, 16.3738)), # Vienna
    # City(11, (47.3769, 8.5417)),  # Zurich
    # City(12, (52.2297, 21.0122)), # Warsaw
    # City(13, (55.7558, 37.6173)), # Moscow
    # City(14, (59.3293, 18.0686)), # Stockholm
    # City(15, (41.3851, 2.1734)),  # Barcelona
    # City(16, (43.2965, 5.3698)),  # Marseille
    # City(17, (45.7640, 4.8357)),  # Lyon
    # City(18, (44.8378, -0.5792)), # Bordeaux
    # City(19, (48.5734, 7.7521)),  # Strasbourg
    # City(20, (43.7102, 7.2620)),  # Nice
]
pop =create_random_population(points, 5)
eval_pop = evaluate_population(pop)
print("\n\nEVALUATED : \n")
i =0
for c in eval_pop:
    i+=1
    print(f"Path {i} : {c[1]} | Score {c[0]}")

selected = roulette_select_population(eval_pop, 3)
print("\n\nSELECTED : \n")
i =0
for c in selected:
    i+=1
    print(f"Path {i} : {c}")