from dataclasses import dataclass, field
from typing import Iterable, Optional

import requests
import numpy as np

from .types import Point


@dataclass
class OSRMConfig:
    host: str = "http://localhost:5000"
    timeout_s: int = 600


def calculate_distance_matrix_m(points: Iterable[Point], config: Optional[OSRMConfig] = None):
    config = config or OSRMConfig()

    if len(points) < 2:
        return 0

    coords_uri = ";".join(["{},{}".format(point.lng, point.lat) for point in points])

    response = requests.get(
        f"{config.host}/table/v1/driving/{coords_uri}?annotations=distance",
        timeout=config.timeout_s,
    )

    response.raise_for_status()

    return np.array(response.json()["distances"])


def calculate_route_distance_m(points: Iterable[Point], config: Optional[OSRMConfig] = None):
    config = config or OSRMConfig()

    if len(points) < 2:
        return 0

    coords_uri = ";".join("{},{}".format(point.lng, point.lat) for point in points)

    response = requests.get(
        f"{config.host}/route/v1/driving/{coords_uri}?annotations=distance&continue_straight=false",
        timeout=config.timeout_s,
    )

    response.raise_for_status()

    return min(r["distance"] for r in response.json()["routes"])
