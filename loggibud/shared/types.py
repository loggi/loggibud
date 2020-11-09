from dataclasses import dataclass
from typing import List

from shapely.geometry import Point as ShapelyPoint


@dataclass
class Point:
    lng: float
    lat: float

    def to_shapely(self):
        return ShapelyPoint(lng, lat)

    @classmethod
    def from_shapely(cls, p):
        return cls(p.x, p.y)


@dataclass
class Delivery:
    point: Point
    size: int


@dataclass
class DeliveryProblemInstance:
    name: str
    deliveries: List[Delivery]
