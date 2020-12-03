from loggibud.v1.types import Point
from loggibud.v1.instance_generation.generators import (
    DeliveryGenerationConfig,
    CVRPGenerationConfig,
    prepare_census_data,
    generate_census_instances,
    generate_deliveries,
    generate_cvrp_subinstances,
)


def test_delivery_instance_generation():
    config = DeliveryGenerationConfig(
        name="rj",
        num_train_instances=3,
        num_dev_instances=2,
        revenue_income_ratio=5e-6,
        num_deliveries_average=100,
        num_deliveries_range=10,
        vehicle_capacity=120,
        max_size=10,
        max_hubs=2,
        save_to="./tests/results/delivery-instances",
    )

    result = generate_census_instances(config)

    assert result
    assert len(result.train_instances) == 3
    assert len(result.dev_instances) == 2
    assert result.deliveries


def test_cvrp_subinstance_generation():
    config = DeliveryGenerationConfig(
        name="rj",
        num_train_instances=3,
        num_dev_instances=2,
        revenue_income_ratio=5e-6,
        num_deliveries_average=100,
        num_deliveries_range=10,
        vehicle_capacity=120,
        max_size=10,
        max_hubs=2,
    )

    instances = generate_census_instances(config)

    config = CVRPGenerationConfig(
        name="rj",
        num_hubs=2,
        num_clusters=10,
        vehicle_capacity=120,
        save_to="./tests/results/cvrp-instances",
    )
    result = generate_cvrp_subinstances(config, instances)

    assert result
    assert len(result.train_instances) == 6
    assert len(result.dev_instances) == 4
