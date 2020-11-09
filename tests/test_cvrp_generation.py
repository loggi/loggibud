from dataclasses import asdict

from dacite import from_dict

from loggibud.cvrp.types import Point
from loggibud.instance_generation.generate import (
    DeliveryGenerationConfig,
    CVRPGenerationConfig,
    prepare_census_data,
    generate_census_instances,
    generate_deliveries,
    generate_cvrp_subinstances,
)


def test_import():
    assert from_dict(Point, asdict(Point(0, 0))) == Point(0, 0)


# def test_census_data_loading():
# 	result = prepare_census_data("rj")

# 	expected_columns = {
# 		"code_tract",
# 		"name_muni",
# 		"total_income",
# 		"geometry",
# 	}

# 	assert expected_columns.issubset(set(result.columns))


def test_delivery_instance_generation():
    config = DeliveryGenerationConfig(
        name="rj",
        num_train_instances=3,
        num_dev_instances=3,
        revenue_income_ratio=5e-6,
        size_average=100,
        size_range=10,
    )

    result = generate_census_instances(config)

    assert result
    assert result.train_instances
    assert result.dev_instances
    assert result.deliveries


def test_cvrp_subinstance_generation():
    config = DeliveryGenerationConfig(
        name="rj",
        num_train_instances=3,
        num_dev_instances=3,
        revenue_income_ratio=5e-6,
        size_average=100,
        size_range=10,
    )

    instances = generate_census_instances(config)

    config = CVRPGenerationConfig(
        name="rj",
        num_hubs=2,
        num_clusters=10,
        random_demand_ratio=0.05,
    )
    result = generate_cvrp_subinstances(config, instances)
    assert result
