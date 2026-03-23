import random
def create_random_population(cities : list, size : int):
    pop = []
    for _ in range(size):
        pop.append(create_sample_random(cities))
    print(f"New population created : {pop}")
    return pop

def create_sample_random(cities : list):
    sample = cities
    shuffled = random.sample(sample, len(sample))
    print(f"sample created : {shuffled}")
    return shuffled

*points = [
    (48.8566, 2.3522),
    (50.1109, 8.6821),
    (52.5200, 13.4050)
]
create_random_population(points, 5)