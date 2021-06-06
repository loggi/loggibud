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
import json
from typing import List, Set
from dataclasses import dataclass

from loggibud.v1.baselines.task_optimal_location.utils.generator_factories import ( 
  pointsClientsGeneratorFactory
)

from loggibud.v1.types import JSONDataclassMixin, Point
from loggibud.v1.distances import calculate_distance_matrix_great_circle_m


logger = logging.getLogger(__name__)
#to show on console
logging.basicConfig(level = logging.INFO)


pointsHashTable = {}

@dataclass
class MinMaxSolution:
  pass


def hashKeyDistance(origin: Point, destination: Point):

  if not (origin, destination) in pointsHashTable:
    matrixDistance = calculate_distance_matrix_great_circle_m([origin, destination])
    pointsHashTable[(origin, destination)] = matrixDistance[0][1]

  return pointsHashTable[(origin, destination)]


def calculateSumDistance(origins: Set[Point], clients: List[Point]):
  sumDistance = 0

  for client in clients:
    minDistance = math.inf

    for origin in origins:
      dist = hashKeyDistance(origin, client)

      if dist < minDistance:
        minDistance = dist

    sumDistance += minDistance
      
  return sumDistance

def solve(instancesFactory, candidates: List[Point]):
  #set comprehension
  origins = { i.origin for i in instancesFactory() }

  pointsClientsFactory = pointsClientsGeneratorFactory(instancesFactory)

  currentMinSum = calculateSumDistance(origins, pointsClientsFactory())
  
  logger.info(f"The current MinSum is: {currentMinSum}")
  
  minSumSolutionCandidates = []
  minSumCandidate = (currentMinSum, 0)

  for candidate in candidates:
    originsWithCandidates = origins.union([candidate])

    newMinSumCandidate = calculateSumDistance(originsWithCandidates, pointsClientsFactory())
    minSumSolutionCandidates.append((newMinSumCandidate, candidate))
    
    if newMinSumCandidate < minSumCandidate[0]:
      minSumCandidate = (newMinSumCandidate, candidate)

  logger.info(f"Recalculating, we've got those solutions: {minSumSolutionCandidates}")

  logger.info(f"The best solution was: {minSumCandidate}")

  return (currentMinSum, minSumCandidate)
  

# import timeit
# start = timeit.default_timer()


if __name__ == '__main__':
  from loggibud.v1.baselines.task_optimal_location.utils.generator_factories import (
    instancesGeneratorFactory
  )

  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument("--location_id", type=str, required=True)
  args = parser.parse_args()


  paths = []
  with open('./loggibud/v1/baselines/task_optimal_location/resolved_paths.json') as dir:
    paths = json.load(dir)[args.location_id]


  instances = instancesGeneratorFactory(paths)

  candidates = [
    Point(lat=-15.7621978, lng=-47.9137767),
    Point(lat=-15.7035628, lng=-47.8781157)
  ]

  solve(instances, candidates)
