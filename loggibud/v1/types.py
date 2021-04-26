import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Union

from dacite import from_dict


class JSONDataclassMixin:
    """Mixin for adding JSON file capabilities to Python dataclasses."""

    @classmethod
    def from_file(cls, path: Union[Path, str]) -> "JSONDataclassMixin":
        """Load dataclass instance from provided file path."""

        with open(path) as f:
            data = json.load(f)

        return from_dict(cls, data)

    def to_file(self, path: Union[Path, str]) -> None:
        """Save dataclass instance to provided file path."""

        with open(path, "w") as f:
            json.dump(asdict(self), f)

        return


@dataclass(unsafe_hash=True)
class Point:
    """Point in earth. Assumes a geodesical projection."""

    lng: float
    """Longitude (x axis)."""

    lat: float
    """Latitude (y axis)."""


@dataclass(unsafe_hash=True)
class Delivery:
    """A delivery request."""

    id: str
    """Unique id."""

    point: Point
    """Delivery location."""

    size: int
    """Size it occupies in the vehicle (considered 1-D for simplicity)."""


@dataclass
class DeliveryProblemInstance(JSONDataclassMixin):
    name: str
    """Unique name of this instance."""

    region: str
    """Region name."""

    max_hubs: int
    """Maximum number of hubs allowed in the solution."""

    vehicle_capacity: int
    """Maximum sum of sizes per vehicle allowed in the solution."""

    deliveries: List[Delivery]
    """List of deliveries to be solved."""


@dataclass
class CVRPInstance(JSONDataclassMixin):
    name: str
    """Unique name of this instance."""

    region: str
    """Region name."""

    origin: Point
    """Location of the origin hub."""

    vehicle_capacity: int
    """Maximum sum of sizes per vehicle allowed in the solution."""

    deliveries: List[Delivery]
    """List of deliveries to be solved."""


@dataclass
class CVRPSolutionVehicle:

    origin: Point
    """Location of the origin hub."""

    deliveries: List[Delivery]
    """Ordered list of deliveries from the vehicle."""

    @property
    def circuit(self) -> List[Point]:
        return (
            [self.origin] + [d.point for d in self.deliveries] + [self.origin]
        )

    @property
    def occupation(self) -> int:
        return sum([d.size for d in self.deliveries])


@dataclass
class CVRPSolution(JSONDataclassMixin):
    name: str
    vehicles: List[CVRPSolutionVehicle]

    @property
    def deliveries(self):
        return [d for v in self.vehicles for d in v.deliveries]
