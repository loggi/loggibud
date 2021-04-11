import json

import pytest
from dacite import from_dict
from mock import patch

from loggibud.v1 import data_conversion
from loggibud.v1.distances import calculate_distance_matrix_great_circle_m
from loggibud.v1.types import CVRPInstance


@pytest.fixture
def toy_cvrp_instance():
    with open("tests/results/cvrp-instances/train/rj-0/cvrp-0-rj-0.json") as f:
        data = json.load(f)

    return from_dict(CVRPInstance, data)


@pytest.fixture
def mocked_osrm_distance_matrix():
    """Monkey-patch the OSRM distance matrix with the Great Circle"""

    with patch(
        "loggibud.v1.data_conversion.calculate_distance_matrix_m",
        new=calculate_distance_matrix_great_circle_m,
    ) as mock_osrm:
        yield mock_osrm


def test_can_create_proper_tsplib_from_instance(
    toy_cvrp_instance, mocked_osrm_distance_matrix
):
    tspfile = data_conversion.to_tsplib(toy_cvrp_instance)

    assert toy_cvrp_instance.name in tspfile
    assert "ACVRP" in tspfile
    assert str(toy_cvrp_instance.vehicle_capacity) in tspfile
