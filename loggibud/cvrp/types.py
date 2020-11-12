from typing import List
from dataclasses import dataclass

from ..shared.types import Point, Delivery


@dataclass
class CVRPInstance:
    name: str

    origin: Point
    deliveries: List[Delivery]

    vehicle_capacity: int
    distance_matrix_m: List[List[float]]


@dataclass
class CVRPSolutionVehicle:
    demand_indexes: List[int]


@dataclass
class CVRPSolution:
    name: str
    vehicles: List[CVRPSolutionVehicle]
