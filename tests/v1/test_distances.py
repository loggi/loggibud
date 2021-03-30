import json

import numpy as np
import pytest
from dacite import from_dict

from loggibud.v1.distances import calculate_distance_matrix_great_circle_m
from loggibud.v1.types import CVRPInstance


@pytest.fixture
def toy_cvrp_instance():
    with open("tests/results/cvrp-instances/train/rj-0/cvrp-0-rj-0.json") as f:
        data = json.load(f)

    return from_dict(CVRPInstance, data)


def test_great_circle_distance(toy_cvrp_instance):
    """
    Ensure that the distance matrix has proper dimensions and the distances
    between each point to itself is zero.
    """
    points = [delivery.point for delivery in toy_cvrp_instance.deliveries]

    distance_matrix = calculate_distance_matrix_great_circle_m(points)

    num_points = len(points)
    assert distance_matrix.shape == (num_points, num_points)
    assert np.array_equal(np.diag(distance_matrix), np.zeros(num_points))
