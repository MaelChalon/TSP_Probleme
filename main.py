from clientHTTP.ClientHTTP import ClientHTTP
from TSP import *


def main() -> None:
    client = ClientHTTP()

    test_instance_id = "regions"
    instance = client.get_instance(test_instance_id)

    cities = instance.get("cities", [])
    list_cities = [
        City(index, (latitude, longitude))
        for index, (longitude, latitude) in enumerate(cities)
    ]

    result = solve_tsp(list_cities, 100, 100)

    http_result = [city.id for city in result]

    score = eval_dist(extract_coords(result))
    print(score)
    print(http_result)

    with open("resultats.txt", "a", encoding="utf-8") as file:
        file.write(f"{test_instance_id} : {score}, {http_result}\n")



if __name__ == "__main__":
    main()
