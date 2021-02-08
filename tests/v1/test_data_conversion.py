import json

import pytest
from dacite import from_dict

from loggibud.v1 import data_conversion
from loggibud.v1.types import CVRPInstance


@pytest.fixture
def toy_cvrp_instance():
    with open("tests/results/cvrp-instances/train/rj-0/cvrp-0-rj-0.json") as f:
        data = json.load(f)

    return from_dict(CVRPInstance, data)


def test_can_create_proper_tsplib_from_instance(toy_cvrp_instance):
    tspfile = data_conversion.to_tsplib(toy_cvrp_instance)

    assert toy_cvrp_instance.name in tspfile
    assert "CVRP" in tspfile
    assert str(toy_cvrp_instance.vehicle_capacity) in tspfile
