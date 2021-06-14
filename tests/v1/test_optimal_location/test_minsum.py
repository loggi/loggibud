from loggibud.v1.types import Point
from loggibud.v1.baselines.task_optimal_location.minsum import solve

def test_minsum_solver(
    mocked_instances,
    mocked_candidates,
    mocked_OLDistance,
    mocked_K
  ):

  (current, solution) = solve(mocked_instances, mocked_candidates, mocked_OLDistance, mocked_K)
  (4206999.083689318, Point(lng=-43.684247, lat=-22.9581481))
  
  assert current == 5123357.986335916

  (solutionSum, solutionPoint) = solution
  assert solutionSum == 4206999.083689318
  assert solutionPoint == Point(lng=-43.684247, lat=-22.9581481)

  