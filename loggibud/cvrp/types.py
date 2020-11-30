import json
from pathlib import Path
from typing import List, Union
from dataclasses import dataclass, asdict

from dacite import from_dict

from ..shared.types import Point, Delivery, JSONDataclassMixin





@dataclass
class CVRPInstance(JSONDataclassMixin):
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
class CVRPSolution(JSONDataclassMixin):
    name: str
    vehicles: List[CVRPSolutionVehicle]
