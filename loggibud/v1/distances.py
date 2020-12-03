from dataclasses import dataclass, field
from typing import Iterable

import requests
import numpy as np

from .types import Point


OSRM_HOST = "http://localhost:5000"
OSRM_TIMEOUT = 600


def calculate_distance_matrix_m(points: Iterable[Point]):
    if len(points) < 2:
        return 0

    coords_uri = ";".join(["{},{}".format(point.lng, point.lat) for point in points])

    response = requests.get(
        f"{OSRM_HOST}/table/v1/driving/{coords_uri}?annotations=distance",
        timeout=OSRM_TIMEOUT,
    )

    response.raise_for_status()

    return np.array(response.json()["distances"])


def calculate_route_distance_m(points: Iterable[Point]):
    if len(points) < 2:
        return 0

    coords_uri = ";".join("{},{}".format(point.lng, point.lat) for point in points)

    response = requests.get(
        f"{OSRM_HOST}/route/v1/driving/{coords_uri}?annotations=distance",
        timeout=300,
    )

    response.raise_for_status()

    return response.json()["routes"][0]["distance"]
