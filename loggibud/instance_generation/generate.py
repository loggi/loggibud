import logging
import sys

from loggibud.cvrp.types import Point
from loggibud.instance_generation.generators import (
    DeliveryGenerationConfig,
    CVRPGenerationConfig,
    generate_census_instances,
    generate_cvrp_subinstances,
)


def generate_rj():
    config = DeliveryGenerationConfig(
        name="rj",
        num_train_instances=90,
        num_dev_instances=30,
        revenue_income_ratio=1e-5,
        size_average=28531,
        size_range=4430,
        save_to="./data/delivery-instances",
    )

    delivery_result = generate_census_instances(config)

    config = CVRPGenerationConfig(
        name="rj",
        num_hubs=9,
        num_clusters=256,
        random_demand_ratio=0.01,
        vehicle_capacity=120,
        save_to="./data/cvrp-instances",
    )

    cvrp_result = generate_cvrp_subinstances(config, delivery_result)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generate_rj()
