import json

import pytest
from dacite import from_dict

from loggibud.v1.types import CVRPInstance
from loggibud.v1.baselines.shared import ortools
from loggibud.v1.eval.task1 import evaluate_solution


@pytest.fixture
def toy_cvrp_instance():
    with open("tests/results/cvrp-instances/train/rj-0/cvrp-0-rj-0.json") as f:
        data = json.load(f)

    return from_dict(CVRPInstance, data)


def test_delivery_instance_generation(toy_cvrp_instance):
    result = ortools.solve(toy_cvrp_instance)

    evaluate_solution(toy_cvrp_instance, result)
