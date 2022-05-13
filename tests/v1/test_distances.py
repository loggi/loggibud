import numpy as np
import pytest

from loggibud.v1.distances import (
    calculate_distance_matrix_great_circle_m,
    calculate_route_distance_great_circle_m,
)


@pytest.fixture
def toy_cvrp_points(toy_cvrp_instance):
    return [delivery.point for delivery in toy_cvrp_instance.deliveries]


def test_great_circle_distance(toy_cvrp_points):
    """
    Ensure that the distance matrix has proper dimensions and the distances
    between each point to itself is zero.
    """
    distance_matrix = calculate_distance_matrix_great_circle_m(toy_cvrp_points)

    num_points = len(toy_cvrp_points)
    assert distance_matrix.shape == (num_points, num_points)
    assert np.array_equal(np.diag(distance_matrix), np.zeros(num_points))


def test_great_circle_route_distance(toy_cvrp_points):
    """Ensure the total distance is greater than zero"""
    route_distance = calculate_route_distance_great_circle_m(toy_cvrp_points)

    assert route_distance > 0
