"""This module is used to convert the instances to and from known formats
Currently, only TSPLIB is implemented.
"""

from typing import Optional

import numpy as np

from loggibud.v1.distances import calculate_distance_matrix_m
from loggibud.v1.types import CVRPInstance


def to_tsplib(
    instance: CVRPInstance, file_name: Optional[str] = None
) -> Optional[str]:
    """Convert instance into TSPLIB format

    Parameters
    ----------
    instance
        CVRP instance

    file_name
        File with extension ".vrp" to save the instance. If not provided,
        return a string with the same data

    Returns
    -------
    A string with instance data in the TSPLIB format if no ``file_name`` was
    especified, or nothing otherwise
    """

    # Header information
    tspfile = (
        f"NAME : {instance.name}\n"
        "TYPE : ACVRP\n"
        f"DIMENSION : {len(instance.deliveries) + 1}\n"  # + 1 for the origin
        f"CAPACITY : {instance.vehicle_capacity}\n"
        "NODE_COORD_TYPE : TWOD_COORDS\n"
        "EDGE_WEIGHT_TYPE : EXPLICIT\n"
        "EDGE_WEIGHT_FORMAT : FULL_MATRIX\n"
    )

    # Nodes section
    tspfile += (
        "NODE_COORD_SECTION\n"
        f"1 {instance.origin.lng} {instance.origin.lat}\n"  # origin
    )
    tspfile += "\n".join(
        f"{i} {delivery.point.lng} {delivery.point.lat}"
        for i, delivery in enumerate(instance.deliveries, start=2)
    )
    tspfile += "\n"

    # Demand section
    tspfile += "DEMAND_SECTION\n" "1 0\n"
    tspfile += "\n".join(
        f"{i} {delivery.size}"
        for i, delivery in enumerate(instance.deliveries, start=2)
    )
    tspfile += "\n"

    # Depot section: ensure node 1 is the depot (-1 to terminate the list)
    tspfile += "DEPOT_SECTION\n" "1\n" "-1\n"

    # Edge section:
    # Compute distance matrix
    locations = [instance.origin] + [
        delivery.point for delivery in instance.deliveries
    ]
    distance_matrix = (calculate_distance_matrix_m(locations) * 10).astype(
        np.int32
    )

    tspfile += "EDGE_WEIGHT_SECTION\n"

    def print_row(row):
        return " ".join(str(el) for el in row)

    tspfile += "\n".join(print_row(row) for row in distance_matrix)

    if not file_name:
        return tspfile

    with open(file_name, "w") as f:
        f.write(tspfile)
