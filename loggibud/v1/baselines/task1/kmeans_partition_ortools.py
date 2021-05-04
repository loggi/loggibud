"""
This baseline is a simple partioning followed by a routing problem.

It uses pure K-Means to partition the problem into K convex regions and them uses the ORTools solver
to solve each subinstance. It's similar to the method proposed by Ruhan et al. [1], but without the
balancing component.

Refs:

[1] R. He, W. Xu, J. Sun and B. Zu, "Balanced K-Means Algorithm for Partitioning Areas in Large-Scale
Vehicle Routing Problem," 2009 Third International Symposium on Intelligent Information Technology
Application, Shanghai, 2009, pp. 87-90, doi: 10.1109/IITA.2009.307. Available at
https://ieeexplore.ieee.org/abstract/document/5369502.
"""

import logging
from dataclasses import dataclass
from typing import Optional

import numpy as np
from sklearn.cluster import KMeans

from loggibud.v1.types import CVRPInstance, CVRPSolution
from loggibud.v1.baselines.shared.ortools import (
    solve as ortools_solve,
    ORToolsParams,
)


logger = logging.getLogger(__name__)


@dataclass
class KmeansPartitionORToolsParams:
    fixed_num_clusters: Optional[int] = None
    variable_num_clusters: Optional[int] = None
    seed: int = 0

    ortools_params: Optional[ORToolsParams] = None

    @classmethod
    def get_baseline(cls):
        return cls(
            variable_num_clusters=500,
            ortools_params=ORToolsParams(
                time_limit_ms=120_000,
                solution_limit=1_000,
            ),
        )


def solve(
    instance: CVRPInstance,
    params: Optional[KmeansPartitionORToolsParams] = None,
) -> Optional[CVRPSolution]:

    params = params or KmeansPartitionORToolsParams.get_baseline()

    num_deliveries = len(instance.deliveries)
    num_clusters = int(
        params.fixed_num_clusters
        or np.ceil(
            num_deliveries / (params.variable_num_clusters or num_deliveries)
        )
    )

    logger.info(f"Clustering instance into {num_clusters} subinstances")
    clustering = KMeans(num_clusters, random_state=params.seed)

    points = np.array(
        [[d.point.lng, d.point.lat] for d in instance.deliveries]
    )
    clusters = clustering.fit_predict(points)

    delivery_array = np.array(instance.deliveries)

    subsinstance_deliveries = [
        delivery_array[clusters == i] for i in range(num_clusters)
    ]

    subinstances = [
        CVRPInstance(
            name=instance.name,
            deliveries=subinstance.tolist(),
            origin=instance.origin,
            vehicle_capacity=instance.vehicle_capacity,
        )
        for subinstance in subsinstance_deliveries
    ]

    subsolutions = [
        ortools_solve(subinstance, params.ortools_params)
        for subinstance in subinstances
    ]

    return CVRPSolution(
        name=instance.name,
        vehicles=[v for sol in subsolutions for v in sol.vehicles],
    )
