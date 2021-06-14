from loggibud.v1.baselines.task_optimal_location.utils.OLDistance import OLDistance
import pytest

from loggibud.v1.types import Point
from loggibud.v1.baselines.task_optimal_location.utils.generator_factories import (
  instancesGeneratorFactory
)

@pytest.fixture
def mocked_instances():
    instance = instancesGeneratorFactory([
      "tests/test_instances", 
    ])
    return instance

@pytest.fixture
def mocked_candidates():
  pointsClients = [
    Point(lat=-22.9666855, lng=-43.6941723),
    Point(lat=-22.9581481, lng=-43.684247)
  ]
  return pointsClients

@pytest.fixture
def mocked_OLDistance():
  return OLDistance("distance_matrix_great_circle")
  

@pytest.fixture
def mocked_K():
  return 1
  
