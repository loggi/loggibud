from dataclasses import dataclass
from typing import Iterable, Optional, Any

import requests
import numpy as np

from .types import Point


EARTH_RADIUS_METERS = 6371000


@dataclass
class OSRMConfig:
    host: str = "http://localhost:5000"
    timeout_s: int = 600


def calculate_distance_matrix_m(
    points: Iterable[Point], config: Optional[OSRMConfig] = None
):
    config = config or OSRMConfig()

    if len(points) < 2:
        return 0

    coords_uri = ";".join(
        ["{},{}".format(point.lng, point.lat) for point in points]
    )

    response = requests.get(
        f"{config.host}/table/v1/driving/{coords_uri}?annotations=distance",
        timeout=config.timeout_s,
    )

    response.raise_for_status()

    return np.array(response.json()["distances"])


def calculate_route_distance_m(
    points: Iterable[Point], config: Optional[OSRMConfig] = None
):
    config = config or OSRMConfig()

    if len(points) < 2:
        return 0

    coords_uri = ";".join(
        "{},{}".format(point.lng, point.lat) for point in points
    )

    response = requests.get(
        f"{config.host}/route/v1/driving/{coords_uri}?annotations=distance&continue_straight=false",
        timeout=config.timeout_s,
    )

    response.raise_for_status()

    return min(r["distance"] for r in response.json()["routes"])


def calculate_distance_matrix_great_circle_m(
    points: Iterable[Point], config: Any = None
) -> np.ndarray:
    """Distance matrix using the Great Circle distance
    This is an Euclidean-like distance but on spheres [1]. In this case it is
    used to estimate the distance in meters between locations in the Earth.

    Parameters
    ----------
    points
        Iterable with `lat` and `lng` properties with the coordinates of a
        delivery

    Returns
    -------
    distance_matrix
        Array with the (i, j) entry indicating the Great Circle distance (in
        meters) between the `i`-th and the `j`-th point

    References
    ----------
    [1] https://en.wikipedia.org/wiki/Great-circle_distance
    Using the third computational formula
    """
    points_rad = np.radians([(point.lat, point.lng) for point in points])

    delta_lambda = points_rad[:, [1]] - points_rad[:, 1]  # (N x M) lng
    phi1 = points_rad[:, [0]]  # (N x 1) array of source latitudes
    phi2 = points_rad[:, 0]  # (1 x M) array of destination latitudes

    delta_sigma = np.arctan2(
        np.sqrt(
            (np.cos(phi2) * np.sin(delta_lambda)) ** 2
            + (
                np.cos(phi1) * np.sin(phi2)
                - np.sin(phi1) * np.cos(phi2) * np.cos(delta_lambda)
            )
            ** 2
        ),
        (
            np.sin(phi1) * np.sin(phi2)
            + np.cos(phi1) * np.cos(phi2) * np.cos(delta_lambda)
        ),
    )

    return EARTH_RADIUS_METERS * delta_sigma


def calculate_route_distance_great_circle_m(points: Iterable[Point]) -> float:
    """Compute total distance from moving from starting point to final
    The total distance will be from point 0 to 1, from 1 to 2, and so on in
    the order provided.

    Parameters
    ----------
    points
        Iterable with `lat` and `lng` properties with the coordinates of a
        delivery

    Returns
    -------
    route_distance
        Total distance from going to the first point to the next until the last
        one
    """

    distance_matrix = calculate_distance_matrix_great_circle_m(points)

    point_indices = np.arange(len(points))

    return distance_matrix[point_indices[:-1], point_indices[1:]].sum()
