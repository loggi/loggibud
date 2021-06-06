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
from typing import List, Generator

from loggibud.v1.types import Point
from loggibud.v1.distances import calculate_distance_matrix_great_circle_m

from loggibud.v1.baselines.task_optimal_location.utils.generator_factories import (
  pointsClientsGeneratorFactory
)


logger = logging.getLogger(__name__)
#to show on console
logging.basicConfig(level = logging.INFO)


pointsHashTable = {}

def hashKeyDistance(origin: Point, destination: Point):

  if not (origin, destination) in pointsHashTable:
    matrixDistance = calculate_distance_matrix_great_circle_m([origin, destination])
    pointsHashTable[(origin, destination)] = matrixDistance[0][1]

  return pointsHashTable[(origin, destination)]


def calculateMaxMinDistance(origins: List[Point], clients: Generator[Point]):
  maxDistance = 0

  for client in clients:

    minDistance = math.inf

    for origin in origins:
      dist = hashKeyDistance(origin, client)
      if dist < minDistance:
        minDistance = dist
        originMin = origin
        clientMin = client

    if minDistance > maxDistance:
      maxDistance = minDistance
      originMax = originMin
      clientMax = clientMin
      
  return (maxDistance, originMax, clientMax)


def solve(instancesFactory, candidates: List[Point]):
  origins = { i.origin for i in instancesFactory() }

  pointsClientsFactory = pointsClientsGeneratorFactory(instancesFactory)

  currentMaxSolution = calculateMaxMinDistance(origins, pointsClientsFactory())
  
  logger.info(f"The Current MaxSolution is: {currentMaxSolution}")
  
  maxSolutionCandidates = []
  minDistanceCandidate = currentMaxSolution

  for candidate in candidates:
    originsWithCandidates = origins.union([candidate])
    
    (maxDistance, origin, client) = calculateMaxMinDistance(originsWithCandidates, pointsClientsFactory())
    maxSolutionCandidates.append((maxDistance, origin, client))
    
    if maxDistance < minDistanceCandidate[0]:
      minDistanceCandidate = (maxDistance, origin, client)

  logger.info(f"Recalculating, we've got those solutions: {maxSolutionCandidates}")

  logger.info(f"The best solution was: {minDistanceCandidate}")

  return (currentMaxSolution, minDistanceCandidate)



if __name__ == '__main__':
  from loggibud.v1.baselines.task_optimal_location.utils.generator_factories import (
    instancesGeneratorFactory
  )

  paths = ["./tests/test_instances"]

  instances = instancesGeneratorFactory(paths)

  candidates = [
    Point(lat=-22.9666855, lng=-43.6941723),
    Point(lat=-22.9581481, lng=-43.684247)
  ]

  solve(instances, candidates)