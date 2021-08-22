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
