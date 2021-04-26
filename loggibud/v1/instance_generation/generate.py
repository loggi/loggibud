import logging

from .generators import (
    DeliveryGenerationConfig,
    CVRPGenerationConfig,
    generate_census_instances,
    generate_cvrp_subinstances,
)

DELIVERY_CONFIGS = {
    "rj": DeliveryGenerationConfig(
        name="rj",
        num_train_instances=90,
        num_dev_instances=30,
        revenue_income_ratio=1e-4,
        num_deliveries_average=28531,
        num_deliveries_range=4430,
        vehicle_capacity=180,
        max_size=10,
        max_hubs=7,
        save_to="./data/delivery-instances-1.0",
    ),
    "df": DeliveryGenerationConfig(
        name="df",
        num_train_instances=90,
        num_dev_instances=30,
        revenue_income_ratio=1e-4,
        num_deliveries_average=9865,
        num_deliveries_range=2161,
        vehicle_capacity=180,
        max_size=10,
        max_hubs=3,
        save_to="./data/delivery-instances-1.0",
    ),
    "pa": DeliveryGenerationConfig(
        name="pa",
        num_train_instances=90,
        num_dev_instances=30,
        revenue_income_ratio=1e-4,
        num_deliveries_average=4510,
        num_deliveries_range=956,
        vehicle_capacity=180,
        max_size=10,
        max_hubs=2,
        save_to="./data/delivery-instances-1.0",
    ),
}


CVRP_CONFIGS = {
    "rj": CVRPGenerationConfig(
        name="rj",
        num_hubs=6,
        num_clusters=256,
        vehicle_capacity=180,
        save_to="./data/cvrp-instances-1.0",
    ),
    "df": CVRPGenerationConfig(
        name="df",
        num_hubs=3,
        num_clusters=256,
        vehicle_capacity=180,
        save_to="./data/cvrp-instances-1.0",
    ),
    "pa": CVRPGenerationConfig(
        name="pa",
        num_hubs=2,
        num_clusters=256,
        vehicle_capacity=180,
        save_to="./data/cvrp-instances-1.0",
    ),
}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    for instance in DELIVERY_CONFIGS:
        config = DELIVERY_CONFIGS[instance]
        delivery_result = generate_census_instances(config)

        cvrp_config = CVRP_CONFIGS.get(instance)

        if cvrp_config:
            generate_cvrp_subinstances(cvrp_config, delivery_result)
