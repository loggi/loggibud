"""
This baseline is a simple partioning followed by a routing problem.

It uses pure K-Means to partition the problem into K regions and them uses the ORTools solver to solve
each subinstance. It's similar to the method proposed by Ruhan et al [1], but without the balancing
component, as we observed that most instances are already well balanced and far beyond vehicle capacity.

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
from sklearn.cluster import MiniBatchKMeans

from loggibud.v1.types import (
    CVRPInstance,
    CVRPSolution,
    CVRPSolutionVehicle,
    Delivery,
)
from ..shared.ortools import solve_cvrp as ortools_solve, ORToolsParams


logger = logging.getLogger(__name__)


@dataclass
class KmeansAggregateORToolsParams:
    fixed_num_clusters: Optional[int] = None
    variable_num_clusters: Optional[int] = None
    seed: int = 0

    cluster_ortools_params: Optional[ORToolsParams] = None
    aggregate_ortools_params: Optional[ORToolsParams] = None

    @classmethod
    def get_baseline(cls):
        return cls(
            variable_num_clusters=100,
            cluster_ortools_params=ORToolsParams(
                solution_limit=300,
                time_limit_ms=10_000,
            ),
        )


def solve(
    instance: CVRPInstance,
    params: Optional[KmeansAggregateORToolsParams] = None,
) -> Optional[CVRPSolution]:

    params = params or KmeansAggregateORToolsParams.get_baseline()

    num_deliveries = len(instance.deliveries)
    num_clusters = int(
        params.fixed_num_clusters
        or np.ceil(num_deliveries / (params.variable_num_clusters or 1))
    )

    logger.info(f"Clustering instance into {num_clusters} subinstances")
    clustering = MiniBatchKMeans(num_clusters, random_state=params.seed)

    points = np.array(
        [[d.point.lng, d.point.lat] for d in instance.deliveries]
    )
    clusters = clustering.fit_predict(points)

    delivery_array = np.array(instance.deliveries)

    deliveries_per_cluster = [
        delivery_array[clusters == i] for i in range(num_clusters)
    ]

    def solve_cluster(deliveries):
        if len(deliveries) < 2:
            return [deliveries]

        cluster_instance = CVRPInstance(
            name=instance.name,
            deliveries=deliveries,
            origin=instance.origin,
            vehicle_capacity=instance.vehicle_capacity,
        )

        cluster_solution = ortools_solve(
            cluster_instance, params.cluster_ortools_params
        )

        return [v.deliveries for v in cluster_solution.vehicles]

    def aggregate_deliveries(idx, deliveries):
        return Delivery(
            id=str(idx),
            point=deliveries[0].point,
            size=sum([d.size for d in deliveries]),
        )

    subsolutions = [
        deliveries
        for group in deliveries_per_cluster
        for deliveries in solve_cluster(group.tolist())
        if group.any()
    ]

    aggregated_deliveries = [
        aggregate_deliveries(idx, s) for idx, s in enumerate(subsolutions)
    ]

    aggregated_instance = CVRPInstance(
        name=instance.name,
        deliveries=aggregated_deliveries,
        origin=instance.origin,
        vehicle_capacity=instance.vehicle_capacity,
    )

    aggregated_solution = ortools_solve(aggregated_instance)

    vehicles = [
        CVRPSolutionVehicle(
            origin=v.origin,
            deliveries=[
                d
                for v in solve_cluster(
                    [
                        d
                        for groups in v.deliveries
                        for d in subsolutions[int(groups.id)]
                    ]
                )
                for d in v
            ],
        )
        for v in aggregated_solution.vehicles
    ]

    return CVRPSolution(
        name=instance.name,
        vehicles=vehicles,
    )
