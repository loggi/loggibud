"""
Splits deliveries into regions using a K-Means algorithm. Greedly insert deliveries into
vehicles within a region always assigning the demand to the most constrained vehicle from
the region.
"""

import logging
import os
from dataclasses import dataclass
from typing import Optional, List, Dict
from multiprocessing import Pool
from argparse import ArgumentParser
from pathlib import Path

import numpy as np
from sklearn.cluster import KMeans
from tqdm import tqdm

from loggibud.v1.types import (
    Delivery,
    CVRPInstance,
    CVRPSolution,
    CVRPSolutionVehicle,
)
from loggibud.v1.baselines.shared.ortools import (
    solve as ortools_solve,
    ORToolsParams,
)

logger = logging.getLogger(__name__)


@dataclass
class KMeansGreedyParams:
    fixed_num_clusters: Optional[int] = None
    variable_num_clusters: Optional[int] = None
    seed: int = 0
    ortools_tsp_params: Optional[ORToolsParams] = None

    @classmethod
    def get_baseline(cls):
        return cls(
            fixed_num_clusters=150,
            ortools_tsp_params=ORToolsParams(
                max_vehicles=1,
                time_limit_ms=1_000,
            ),
        )


@dataclass
class KMeansGreedyModel:
    params: KMeansGreedyParams
    clustering: KMeans
    subinstance: Optional[CVRPInstance] = None
    cluster_subsolutions: Optional[Dict[int, List[CVRPSolutionVehicle]]] = None


def pretrain(
    instances: List[CVRPInstance], params: Optional[KMeansGreedyParams] = None
) -> KMeansGreedyModel:
    params = params or KMeansGreedyParams.get_baseline()

    points = np.array(
        [
            [d.point.lng, d.point.lat]
            for instance in instances
            for d in instance.deliveries
        ]
    )

    num_deliveries = len(points)
    num_clusters = int(
        params.fixed_num_clusters
        or np.ceil(
            num_deliveries / (params.variable_num_clusters or num_deliveries)
        )
    )

    logger.info(f"Clustering instance into {num_clusters} subinstances")
    clustering = KMeans(num_clusters, random_state=params.seed)
    clustering.fit(points)

    return KMeansGreedyModel(
        params=params,
        clustering=clustering,
    )


def finetune(
    model: KMeansGreedyModel, instance: CVRPInstance
) -> KMeansGreedyModel:
    """Prepare the model for one particular instance."""

    return KMeansGreedyModel(
        params=model.params,
        clustering=model.clustering,
        cluster_subsolutions={
            i: [] for i in range(model.clustering.n_clusters)
        },
        # Just fill some random instance.
        subinstance=instance,
    )


def route(model: KMeansGreedyModel, delivery: Delivery) -> KMeansGreedyModel:
    """Route a single delivery using the model instance."""

    cluster = model.clustering.predict(
        [[delivery.point.lng, delivery.point.lat]]
    )[0]

    subsolution = model.cluster_subsolutions[cluster]

    def is_feasible(route):
        return (
            route.occupation + delivery.size
            < model.subinstance.vehicle_capacity
        )

    # TODO: We could make this method faster by using a route size table, but seems a bit
    # overkill since it's not a bottleneck.
    feasible_routes = [
        (route_idx, route)
        for route_idx, route in enumerate(subsolution)
        if is_feasible(route)
    ]

    if feasible_routes:
        route_idx, route = max(feasible_routes, key=lambda v: v[1].occupation)

    else:
        route = CVRPSolutionVehicle(
            origin=model.subinstance.origin, deliveries=[]
        )
        subsolution.append(route)
        route_idx = len(subsolution) - 1

    route.deliveries.append(delivery)
    subsolution[route_idx] = route

    return model


def finish(instance: CVRPInstance, model: KMeansGreedyModel) -> CVRPSolution:

    subinstances = [
        CVRPInstance(
            name="",
            region="",
            deliveries=vehicle.deliveries,
            origin=vehicle.origin,
            vehicle_capacity=3 * instance.vehicle_capacity,  # More relaxed.
        )
        for idx, subinstance in enumerate(model.cluster_subsolutions.values())
        for vehicle in subinstance
    ]

    logger.info("Reordering routes.")
    subsolutions = [
        ortools_solve(subinstance, model.params.ortools_tsp_params)
        for subinstance in subinstances
    ]

    return CVRPSolution(
        name=instance.name,
        vehicles=[
            v for subsolution in subsolutions for v in subsolution.vehicles
        ],
    )


def solve_instance(
    model: KMeansGreedyModel, instance: CVRPInstance
) -> CVRPSolution:
    """Solve an instance dinamically using a solver model"""
    logger.info("Finetunning on evaluation instance.")
    model_finetuned = finetune(model, instance)

    logger.info("Starting to dynamic route.")
    for delivery in tqdm(instance.deliveries):
        model_finetuned = route(model_finetuned, delivery)

    return finish(instance, model_finetuned)


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    parser = ArgumentParser()

    parser.add_argument("--train_instances", type=str, required=True)
    parser.add_argument("--eval_instances", type=str, required=True)
    parser.add_argument("--output", type=str)
    parser.add_argument("--params", type=str)

    args = parser.parse_args()

    # Load instance and heuristic params.
    eval_path = Path(args.eval_instances)
    eval_path_dir = eval_path if eval_path.is_dir() else eval_path.parent
    eval_files = (
        [eval_path] if eval_path.is_file() else list(eval_path.iterdir())
    )

    train_path = Path(args.train_instances)
    train_path_dir = train_path if train_path.is_dir() else train_path.parent
    train_files = (
        [train_path] if train_path.is_file() else list(train_path.iterdir())
    )

    # params = params_class.from_file(args.params) if args.params else None

    params = None

    output_dir = Path(args.output or ".")
    output_dir.mkdir(parents=True, exist_ok=True)

    train_instances = [CVRPInstance.from_file(f) for f in train_files[:240]]

    logger.info("Pretraining on training instances.")
    model = pretrain(train_instances)

    def solve(file):
        instance = CVRPInstance.from_file(file)

        logger.info("Finetunning on evaluation instance.")
        model_finetuned = finetune(model, instance)

        logger.info("Starting to dynamic route.")
        for delivery in tqdm(instance.deliveries):
            model_finetuned = route(model_finetuned, delivery)

        solution = finish(instance, model_finetuned)

        solution.to_file(output_dir / f"{instance.name}.json")

    # Run solver on multiprocessing pool.
    with Pool(os.cpu_count()) as pool:
        list(tqdm(pool.imap(solve, eval_files), total=len(eval_files)))
