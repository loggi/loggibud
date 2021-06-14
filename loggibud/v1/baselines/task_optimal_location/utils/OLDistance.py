from dataclasses import dataclass
from loggibud.v1.types import Point
from loggibud.v1.distances import (
  calculate_distance_matrix_m,
  calculate_route_distance_m,
  calculate_distance_matrix_great_circle_m,
  calculate_route_distance_great_circle_m,
  OSRMConfig
)

@dataclass
class OLDistance:
  pointsHashTable = {}
  has_config = False
  is_api = False

  def __init__(self, type):
    self.type = type

    if type == "distance_matrix":
      self.calc_func = calculate_distance_matrix_m
      self.type_response = "matrix"
      self.is_api = True
    elif type == "route_distance":
      self.calc_func = calculate_route_distance_m
      self.type_response = "route"
      self.is_api = True
    elif type == "distance_matrix_great_circle":
      self.calc_func = calculate_distance_matrix_great_circle_m
      self.type_response = "matrix"
    elif type == "route_distance_great_circle":
      self.calc_func = calculate_route_distance_great_circle_m
      self.type_response = "route"

  def config_api(self, **kwargs):
    self.osrm_config = OSRMConfig()

    if kwargs.host:
      self.osrm_config.host = kwargs.host
      self.has_config = True

    if kwargs.timeout:
      self.osrm_config.timeout_s = kwargs.timeout
      self.has_config = True


  def distance(self, origin: Point, destination: Point):
    if not (origin, destination) in self.pointsHashTable:
      
      if self.is_api and self.has_config:
        matrixDistance = self.calc_func([origin, destination], self.osrm_config)
      else:
        matrixDistance = self.calc_func([origin, destination])


      if self.type_response == "matrix":
        self.pointsHashTable[(origin, destination)] = matrixDistance[0][1]

      elif self.type_response == "route":
        self.pointsHashTable[(origin, destination)] = matrixDistance

    return self.pointsHashTable[(origin, destination)]

