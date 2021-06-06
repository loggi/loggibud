from loggibud.v1.types import Point
from loggibud.v1.baselines.task_optimal_location.minsum import solve

def test_minsum_solver(
    mocked_instance,
    mocked_candidates
  ):

  (current, solution) = solve(mocked_instance, mocked_candidates)
  (4206999.083689318, Point(lng=-43.684247, lat=-22.9581481))
  
  assert current == 5123357.986335916

  (solutionSum, solutionPoint) = solution
  assert solutionSum == 4206999.083689318
  assert solutionPoint == Point(lng=-43.684247, lat=-22.9581481)

  