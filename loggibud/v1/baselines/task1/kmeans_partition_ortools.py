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
import json
import os
from argparse import ArgumentParser
from datetime import timedelta
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional
from multiprocessing import Pool

import numpy as np
from sklearn.cluster import KMeans
from dacite import from_dict
from tqdm import tqdm

from loggibud.v1.types import CVRPInstance, CVRPSolution, CVRPSolutionVehicle
from loggibud.v1.baselines.shared.ortools import (
    solve_cvrp as ortools_solve_cvrp,
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
                time_limit_ms=600_000,
                solution_limit=1,
            ),
        )


def solve_cvrp(
    instance: CVRPInstance,
    params: Optional[KmeansPartitionORToolsParams] = None,
) -> Optional[CVRPSolution]:

    params = params or KmeansPartitionORToolsParams.get_baseline()

    num_deliveries = len(instance.deliveries)
    num_clusters = int(
        params.fixed_num_clusters
        or np.ceil(num_deliveries / (params.variable_num_clusters or num_deliveries))
    )

    logger.info(f"Clustering instance into {num_clusters} subinstances")
    clustering = KMeans(num_clusters, random_state=params.seed)

    points = np.array([[d.point.lng, d.point.lat] for d in instance.deliveries])
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
        ortools_solve_cvrp(subinstance, params.ortools_params)
        for subinstance in subinstances
    ]

    return CVRPSolution(
        name=instance.name,
        vehicles=[v for sol in subsolutions for v in sol.vehicles],
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = ArgumentParser()

    parser.add_argument("--instances", type=str, required=True)
    parser.add_argument("--output", type=str)
    parser.add_argument("--params", type=str)

    args = parser.parse_args()

    # Load instance and heuristic params.
    path = Path(args.instances)
    path_dir = path if path.is_dir() else path.parent
    files = [path] if path.is_file() else list(path.iterdir())

    params = (
        KmeansPartitionORToolsParams.from_file(args.params) if args.params else None
    )

    output_dir = Path(args.output or ".")
    output_dir.mkdir(parents=True, exist_ok=True)

    def solve(file):
        instance = CVRPInstance.from_file(file)
        solution = solve_cvrp(instance, params)
        solution.to_file(output_dir / f"{instance.name}.json")

    # Run solver on multiprocessing pool.
    with Pool(8 or os.cpu_count()) as pool:
        list(tqdm(pool.imap(solve, files), total=len(files)))
