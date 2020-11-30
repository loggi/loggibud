import json
from pathlib import Path
from typing import List, Union
from dataclasses import dataclass, asdict

from dacite import from_dict

from ..shared.types import Point, Delivery


class JSONDataclassMixin:
    @classmethod
    def from_file(cls, path: Union[Path, str]) -> "JSONDataclassMixin":
        with open(path) as f:
            data = json.load(f)

        return from_dict(cls, data)

    def to_file(self, path: Union[Path, str]) -> None:
        with open(path, "w") as f:
            json.dump(asdict(self), f)

        return


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
