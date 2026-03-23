from clientHTTP.ClientHTTP import ClientHTTP


def main() -> None:
    client = ClientHTTP()
    instances = client.list_instances()
    print("Instances disponibles :")
    for instance_id, metadata in instances.items():
        print(f"- {instance_id}: {metadata}")

    test_instance_id = "regions"
    instance = client.get_instance(test_instance_id)
    print(f"\nInstance '{test_instance_id}' :")
    print(instance)

    cities = instance.get("cities", [])
    test_tour = list(range(len(cities)))

    result = client.submit_solution(
        student_id="test_client_python",
        instance_id=test_instance_id,
        tour=test_tour,
    )
    print("\nRésultat de la soumission :")
    print(result)

if __name__ == "__main__":
    main()
