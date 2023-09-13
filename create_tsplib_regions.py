from pathlib import Path
from random import sample, seed

from loggibud.v1.data_conversion import to_tsplib_competition
from loggibud.v1.types import CVRPInstance
from loggibud.v1.plotting.plot_instance import plot_cvrp_instance


def join_instances(path, num_deliveries: int, main_instance_index: int):
    """For each path, join all instances into one.
    I will keep the depot of the first one for simplicity.
    """
    instances = [
        CVRPInstance.from_file(instance_file)
        for instance_file in path.iterdir()
    ]

    # Combine all deliveries and extract a subset with `num_deliveries`
    all_deliveries = [
        delivery
        for instance in instances
        for delivery in instance.deliveries
    ]
    deliveries = sample(all_deliveries, k=num_deliveries)

    # Get first instance and update its deliveries
    instance = instances[main_instance_index]
    instance.deliveries = deliveries
    instance.name = f"cvrp-{path.name}-{num_deliveries}"

    return instance


paths_data = [
    (Path("./data/rj"), 1000, 1),
    (Path("./data/rj"), 600, 0),
    (Path("./data/df"), 900, 0),
    (Path("./data/df"), 500, 1),
    (Path("./data/pa"), 600, 0),
    (Path("./data/pa"), 400, 1),
]

if __name__ == "__main__":
    for path, num_deliveries, index in paths_data:
        seed(index)
        instance = join_instances(path, num_deliveries, index)
        plot_cvrp_instance(instance).save(f"{instance.name}.html")
        to_tsplib_competition(instance)
