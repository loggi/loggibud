import json

import pytest
from dacite import from_dict
from mock import patch

from loggibud.v1.types import CVRPInstance
from loggibud.v1.baselines.shared.ortools import ORToolsParams
from loggibud.v1.baselines.task2 import kmeans_greedy, qrp_sweep
from loggibud.v1.distances import (
    calculate_distance_matrix_great_circle_m,
    calculate_route_distance_great_circle_m,
)
from loggibud.v1.eval.task1 import evaluate_solution


@pytest.fixture
def train_instances(toy_cvrp_instance):
    return [toy_cvrp_instance]


@pytest.fixture
def dev_instance():
    with open("tests/test_instances/cvrp-0-rj-3.json") as f:
        data = json.load(f)

    return from_dict(CVRPInstance, data)


@pytest.fixture
def mocked_ortools_osrm_distance_matrix():
    """Monkey-patch the OR-Tools OSRM distance matrix with the Great Circle"""

    with patch(
        "loggibud.v1.baselines.shared.ortools.calculate_distance_matrix_m",
        new=calculate_distance_matrix_great_circle_m,
    ) as mock_osrm:
        yield mock_osrm


@pytest.fixture
def mocked_osrm_route_distance():
    """Monkey-patch the OSRM route distance with the Great Circle"""

    def _mocked_calculate_route_distance_m(points, config=None):
        return calculate_route_distance_great_circle_m(points)

    with patch(
        "loggibud.v1.eval.task1.calculate_route_distance_m",
        new=_mocked_calculate_route_distance_m,
    ) as mock_osrm:
        yield mock_osrm


def test_kmeans_greedy_solver(
    train_instances,
    dev_instance,
    mocked_osrm_route_distance,
    mocked_ortools_osrm_distance_matrix,
):
    # Limit OR-Tools TSP solver to 100 ms (this is just a test, a good solution
    # is not required)
    params = kmeans_greedy.KMeansGreedyParams(
        ortools_tsp_params=ORToolsParams(time_limit_ms=100)
    )
    model = kmeans_greedy.pretrain(train_instances, params=params)
    result = kmeans_greedy.solve_instance(model, dev_instance)

    total_distance = evaluate_solution(dev_instance, result)

    assert total_distance


def test_qrp_sweep_solver(
    train_instances,
    dev_instance,
    mocked_osrm_route_distance,
    mocked_ortools_osrm_distance_matrix,
):
    # Limit OR-Tools TSP solver to 100 ms (this is just a test, a good solution
    # is not required)
    params = qrp_sweep.QRPParams(
        ortools_tsp_params=ORToolsParams(time_limit_ms=100)
    )
    model = qrp_sweep.pretrain(train_instances, params=params)
    result = qrp_sweep.solve_instance(model, dev_instance)

    total_distance = evaluate_solution(dev_instance, result)

    assert total_distance
