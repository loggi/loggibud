import pytest
from mock import patch

from loggibud.v1.distances import calculate_distance_matrix_great_circle_m
from loggibud.v1.instance_generation.generators import (
    DeliveryGenerationConfig,
    CVRPGenerationConfig,
    generate_census_instances,
    generate_cvrp_subinstances,
)

# FIXME: This test module can actually only be run locally in the presence of
# the `raw_data` directory, so it is skipped for now in Github Actions
pytest.skip("Skipping tests requiring raw data", allow_module_level=True)


@pytest.fixture(params=["rj", "df", "pa"])
def instance_name(request):
    return request.param


@pytest.fixture
def mocked_osrm_distance_matrix():
    """Monkey-patch the OSRM distance matrix with the Great Circle"""

    with patch(
        "loggibud.v1.instance_generation.generators.calculate_distance_matrix_m",
        new=calculate_distance_matrix_great_circle_m,
    ) as mock_osrm:
        yield mock_osrm


def test_delivery_instance_generation(instance_name):
    config = DeliveryGenerationConfig(
        name=instance_name,
        num_train_instances=3,
        num_dev_instances=2,
        revenue_income_ratio=1e-6,
        num_deliveries_average=300,
        num_deliveries_range=30,
        vehicle_capacity=180,
        max_size=10,
        max_hubs=2,
        save_to="./tests/results/delivery-instances",
    )

    result = generate_census_instances(config)

    assert result
    assert len(result.train_instances) == 3
    assert len(result.dev_instances) == 2
    assert result.deliveries


def test_cvrp_subinstance_generation(instance_name, mocked_osrm_distance_matrix):
    config = DeliveryGenerationConfig(
        name=instance_name,
        num_train_instances=3,
        num_dev_instances=2,
        revenue_income_ratio=1e-6,
        num_deliveries_average=300,
        num_deliveries_range=30,
        vehicle_capacity=180,
        max_size=10,
        max_hubs=2,
    )

    instances = generate_census_instances(config)

    config = CVRPGenerationConfig(
        name=instance_name,
        num_hubs=2,
        num_clusters=10,
        vehicle_capacity=180,
        save_to="./tests/results/cvrp-instances",
    )
    result = generate_cvrp_subinstances(config, instances)

    assert result
    assert len(result.train_instances) == 6
    assert len(result.dev_instances) == 4
