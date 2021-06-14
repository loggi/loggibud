from loggibud.v1.types import Point
from loggibud.v1.baselines.task_optimal_location.minmax import solve

def test_minsum_solver(
    mocked_instances,
    mocked_candidates
  ):

  (current, solution) = solve(mocked_instances, mocked_candidates)
  (currentMax, currentOrigin, currentClient) = current
  
  assert currentMax == 36831.2314012329
  assert currentOrigin == Point(lng=-43.37769374114032, lat=-22.805996173217757)
  assert currentClient == Point(lng=-43.69207312451086, lat=-22.966707777965688)

  (solutionMax, solutionOrigin, solutionClient) = solution
  assert solutionMax == 27240.58022888479
  assert solutionOrigin == Point(lng=-43.37769374114032, lat=-22.805996173217757)
  assert solutionClient == Point(lng=-43.314351564049836, lat=-22.568088515564767)


  