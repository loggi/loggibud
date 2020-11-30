import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Union

from dacite import from_dict
from shapely.geometry import Point as ShapelyPoint


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


@dataclass(unsafe_hash=True)
class Point:
    lng: float
    lat: float

    def to_shapely(self):
        return ShapelyPoint(lng, lat)

    @classmethod
    def from_shapely(cls, p):
        return cls(p.x, p.y)


@dataclass(unsafe_hash=True)
class Delivery:
    id: str
    point: Point
    size: int


@dataclass
class DeliveryProblemInstance(JSONDataclassMixin):
    name: str
    deliveries: List[Delivery]
    vehicle_capacity: int
    max_hubs: int
