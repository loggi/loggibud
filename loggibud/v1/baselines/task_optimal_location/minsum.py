"""
This baseline implements the MinMax location query [1]
to evaluate a given set of a potential new HUB 

It calculates the nearest (Min) existent Hub 
for each client, and them what's the most distant (Max)
client - HUB between those nearest ones.
After that, it recalculates joining the Candidates Hubies
and check if the Max lowed down

Ref: 
[1] Zitong Chen, Yubao Liu, Raymond Chi-Wing Wong, Jiamin Xiong, 
Ganglin Mai, Cheng Long, "Optimal Location Queries in Road Networks", 
ACM Transactions on Database Systems (TODS), vol. 40, pp. 1, 2015.
"""
import logging
import math
import heapq

from typing import List, Set

from loggibud.v1.baselines.task_optimal_location.utils.generator_factories import ( 
  pointsClientsGeneratorFactory
)
from loggibud.v1.baselines.task_optimal_location.utils.OLDistance import (
  OLDistance
)

from loggibud.v1.types import Point

logger = logging.getLogger(__name__)
#to show on console
logging.basicConfig(level = logging.INFO)

def calculateSumDistance(origins: Set[Point], clients: List[Point], old: OLDistance):
  sumDistance = 0

  for client in clients:
    minDistance = math.inf

    for origin in origins:
      dist = old.distance(origin, client)

      if dist < minDistance:
        minDistance = dist

    sumDistance += minDistance
      
  return sumDistance

def solve(instancesFactory, candidates: List[Point], old: OLDistance, k: int):
  #set comprehension
  origins = { i.origin for i in instancesFactory() }

  pointsClientsFactory = pointsClientsGeneratorFactory(instancesFactory)

  currentMinSum = calculateSumDistance(origins, pointsClientsFactory(), old)
  
  logger.info(f"The current MinSum is: {currentMinSum}")
  
  minSumSolutionCandidates = []
  i = 0

  for candidate in candidates:
    originsWithCandidates = origins.union([candidate])

    newMinSumCandidate = calculateSumDistance(originsWithCandidates, pointsClientsFactory(), old)
    heapq.heappush(minSumSolutionCandidates, (newMinSumCandidate, i, candidate))
    i = i + 1

  minKSumSolution = [] 

  for i in range(k):
    s = heapq.heappop(minSumSolutionCandidates)
    minKSumSolution.append((s[0], s[2]))

  logger.info(f"Recalculating, we've got those solutions: {minSumSolutionCandidates}")

  logger.info(f"The best K:{k} solution was: {minKSumSolution}")

  return (currentMinSum, minKSumSolution)


if __name__ == '__main__':
  from loggibud.v1.baselines.task_optimal_location.utils.generator_factories import (
    instancesGeneratorFactory
  )
  from loggibud.v1.baselines.task_optimal_location.utils.resolve_arg import (
    resolve_location_id,
    resolve_candidates,
    resolve_calc_method,
    resolve_K
  )

  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument("--location_id", type=str, required=True)
  parser.add_argument("--candidates", nargs="+", type=float, required=True)
  parser.add_argument("--calc_method", type=str, required=False)
  parser.add_argument("--k", type=int, required=False)
  args = parser.parse_args()

  try:
    paths = resolve_location_id(args.location_id)

    instances = instancesGeneratorFactory(paths)

    (candidates, len_candidates) = resolve_candidates(args.candidates)

    old = resolve_calc_method(args.calc_method)

    k = resolve_K(args.k, len_candidates)

  except ValueError as e:
    logging.error(e)
    exit()

  solve(instances, candidates, old, k)
