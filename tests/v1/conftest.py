import json

import pytest
from dacite import from_dict

from loggibud.v1.types import CVRPInstance


@pytest.fixture
def toy_cvrp_instance():
    with open("tests/test_instances/cvrp-0-rj-0.json") as f:
        data = json.load(f)

    return from_dict(CVRPInstance, data)
