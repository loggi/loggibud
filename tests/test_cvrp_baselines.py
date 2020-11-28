import json

import pytest
from dacite import from_dict

from loggibud.cvrp.types import Point, CVRPInstance
from loggibud.cvrp.baselines import ortools1
from loggibud.cvrp.eval import evaluate_cvrp_solution


@pytest.fixture
def toy_cvrp_instance():
    with open("tests/results/cvrp-instances/train/rj-0-cvrp-0.json") as f:
        data = json.load(f)

    return from_dict(CVRPInstance, data)


def test_delivery_instance_generation(toy_cvrp_instance):
    result = ortools1.solve_cvrp(toy_cvrp_instance)

    evaluate_cvrp_solution(toy_cvrp_instance, result)
