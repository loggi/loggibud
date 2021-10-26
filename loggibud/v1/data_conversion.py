"""This module is used to convert the instances to and from known formats
Currently, only TSPLIB is implemented.
"""

from typing import Optional
from dataclasses import dataclass

import tsplib95
import numpy as np

from loggibud.v1.distances import calculate_distance_matrix_m, OSRMConfig
from loggibud.v1.types import CVRPInstance, JSONDataclassMixin


@dataclass
class TSPLIBConversionParams(JSONDataclassMixin):

    osrm_config: Optional[OSRMConfig] = None
    """Config for calling OSRM distance service."""

    distance_scaling_factor: int = 10
    """
    Scaling factor for distance matrixes. Scaling is required for solvers that
    operate with integer or fixed point distances.
    """


def to_tsplib(
    instance: CVRPInstance, params: Optional[TSPLIBConversionParams] = None
) -> tsplib95.models.StandardProblem:

    params = params or TSPLIBConversionParams()

    num_deliveries = len(instance.deliveries)

    demands_section = {
        i: delivery.size
        for i, delivery in enumerate(instance.deliveries, start=2)
    }

    # Depot demand is always zero.
    demands_section[1] = 0

    locations = [instance.origin] + [
        delivery.point for delivery in instance.deliveries
    ]

    distance_matrix = calculate_distance_matrix_m(
        locations, config=params.osrm_config
    )
    scaled_matrix = distance_matrix * params.distance_scaling_factor

    problem = tsplib95.models.StandardProblem(
        name=instance.name,
        type="ACVRP",
        dimension=num_deliveries + 1,
        edge_weight_type="EXPLICIT",
        edge_weight_format="FULL_MATRIX",
        edge_weights=scaled_matrix.astype(np.int32).tolist(),
        demands=demands_section,
        capacity=instance.vehicle_capacity,
    )

    return problem


def to_tsplib_competition(
    instance: CVRPInstance, params: Optional[TSPLIBConversionParams] = None
) -> tsplib95.models.StandardProblem:
    """Converts a LoggiBUD instance into a TSPLIB95 competition format

    Notes
    -----
    Here are specific details for the competition:
        - The distance matrix must be symmetric: in this case, replace the
        (i, j)-th element with the average of the (j, i)-th and itself;
        - The coordinates must be added in the `NODE_COORD_SECTION`;
        - The distance matrix is explicitly written with a `LOWER_DIAG_ROW`
        format.
    """

    params = params or TSPLIBConversionParams()

    num_deliveries = len(instance.deliveries)

    demands_section = {
        i: delivery.size
        for i, delivery in enumerate(instance.deliveries, start=2)
    }

    # Depot demand is always zero.
    demands_section[1] = 0

    locations = [instance.origin] + [
        delivery.point for delivery in instance.deliveries
    ]

    # Create a symmetric distance matrix by replace the (i, j) element with the
    # average of (i, j) and (j, i)
    distance_matrix = calculate_distance_matrix_m(
        locations, config=params.osrm_config
    )
    symmetric_distance_matrix = (
        np.triu(distance_matrix) + np.tril(distance_matrix).T
    ) / 2  # upper triangular portion
    symmetric_distance_matrix += np.triu(
        symmetric_distance_matrix, k=-1
    ).T  # lower triangular portion
    scaled_matrix = symmetric_distance_matrix * params.distance_scaling_factor

    # Not well documented, but the API seems to expect a dict mapping location
    # index with its coordinates
    node_coords = {
        i: (location.lng, location.lat)
        for i, location in enumerate(locations, start=1)
    }

    # For each row of the distance matrix, write only the elements up to the
    # main diagonal
    scaled_matrix_triu = np.tril(scaled_matrix.astype(np.int32)).tolist()
    edge_weights = [
        row[:i] for i, row in enumerate(scaled_matrix_triu, start=1)
    ]

    problem = tsplib95.models.StandardProblem(
        name=instance.name,
        type="CVRP",
        dimension=num_deliveries + 1,
        node_coords=node_coords,
        edge_weight_type="EXPLICIT",
        edge_weight_format="LOWER_DIAG_ROW",
        edge_weights=edge_weights,
        demands=demands_section,
        capacity=instance.vehicle_capacity,
        depots=[1],
    )

    return problem
