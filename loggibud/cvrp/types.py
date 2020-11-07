from typing import List
from dataclasses import dataclass

from ..shared.types import Point


@dataclass
class CVRPDemand:
    point: Point
    demand: int


@dataclass
class CVRPInstance:
    name: str

    origin: Point
    demands: List[CVRPDemand]

    vehicle_capacity: int


@dataclass
class CVRPSolutionVehicle:
    demand_indexes: List[int]


@dataclass
class CVRPSolution:
    name: str
    vehicles: List[CVRPSolutionVehicle]
