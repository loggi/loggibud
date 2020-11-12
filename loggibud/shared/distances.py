from dataclasses import dataclass, field
from typing import Iterable

import requests
import numpy as np

from .types import Point


OSRM_HOST = "http://ec2-34-222-175-250.us-west-2.compute.amazonaws.com"
OSRM_HOST = "http://router.project-osrm.org"
OSRM_TIMEOUT = 600


def calculate_distance_matrix_m(points: Iterable[Point]):
    if len(points) < 2:
        return 0

    coords_uri = ";".join(["{},{}".format(point.lng, point.lat) for point in points])

    response = requests.get(
        f"{OSRM_HOST}/table/v1/driving/{coords_uri}?annotations=distance,duration",
        timeout=OSRM_TIMEOUT,
    )

    response.raise_for_status()

    return np.array(response.json()["distances"])
