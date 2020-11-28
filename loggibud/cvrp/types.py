from typing import List
from dataclasses import dataclass

from ..shared.types import Point, Delivery


@dataclass
class CVRPInstance:
    name: str

    origin: Point
    deliveries: List[Delivery]

    vehicle_capacity: int


@dataclass
class CVRPSolutionVehicle:

    origin: Point

    deliveries: List[Delivery]
    """Ordered list of deliveries from the vehicle."""

    @property
    def circuit(self) -> List[Point]:
        return [self.origin] + [d.point for d in self.deliveries] + [self.origin]


@dataclass
class CVRPSolution:
    name: str
    vehicles: List[CVRPSolutionVehicle]
