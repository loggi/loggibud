from loggibud.v1.baselines.task_optimal_location.utils.OLDistance import OLDistance
from loggibud.v1.types import Point
import os

def resolve_location_id(id: str):
  instances_dir = "./data/cvrp-instances-1.0/dev"

  paths = [
    os.path.join(instances_dir, path)
    for path in os.listdir(instances_dir) if path.startswith(id)
  ]

  if len(paths) == 0:
    raise ValueError("Location ID not found. Please provide a valid ID")

  return paths


def resolve_candidates(args):
  size = len(args)
  if size == 0:
    raise ValueError("Candidates not provided. Please insert a list of candidates")

  if not size % 2 == 0:
    raise ValueError("The number of coordinates must be even.")

  candidates = []

  for i in range(0, size, 2):
    candidates.append(Point(args[i], args[i+1]))
  
  return candidates

def resolve_calc_method(calc_method):
  valid_calc_methods = ["distance_matrix", "route_distance", "distance_matrix_great_circle", "route_distance_great_circle"]

  if calc_method == None:
    calc_method = "distance_matrix_great_circle"

  if not calc_method in valid_calc_methods:
    raise ValueError(f"Invalid calc_method. The method should be {valid_calc_methods}, and if not provided distance_matrix_great_circle will be setted by default")

  return OLDistance(calc_method)
