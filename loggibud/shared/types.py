from dataclasses import dataclass
from typing import List

from shapely.geometry import Point as ShapelyPoint


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
class DeliveryProblemInstance:
    name: str
    deliveries: List[Delivery]
