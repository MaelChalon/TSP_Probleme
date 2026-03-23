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
        score = eval_dist(sample)
        elem = (score, sample)
        result.append(elem)
    return result

points = [
    City(1, (48.8566, 2.3522)),
    City(2,(50.1109, 8.6821)),
    City(3, (52.5200, 13.4050))
]
create_random_population(points, 5)