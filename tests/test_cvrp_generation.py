from dataclasses import asdict

from dacite import from_dict

from loggibud.cvrp.types import Point


def test_import():
    assert from_dict(Point, asdict(Point(0, 0))) == Point(0, 0)
