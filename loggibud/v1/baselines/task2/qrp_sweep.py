"""qRP-Sweep: Capacitated Region Partitioning with a Sweep method
This method is based on [1] and [2], and has the following simple structure.

Algorithm
---------
There is a "planning" phase in which we divide the delivery region into
`num_clusters` sub-regions. Then, in the "execution" phase, we route each
incoming package to its closest sub-region, and add it to a vehicle. This is
repeated until each vehicle is full, when a TSP is solved.

Besides being an old reference, it became the basis for many recent methods. In
fact, the difference among them is in how we define the sub-regions. According
to [1], the only constraint is that each one has the same probability of having
a new incoming package.

To achieve that, we follow here the sweep method of [2]. Basically, think about
a circle centered at the centroid of the historical deliveries. We can convert
the demands into polar coordinates, each one with angles in the interval
[-pi, pi]. The sweep method consists in spliting this interval into
`n_clusters` sub-intervals, each one having almost the same number of packages.

Assumptions
-----------
The number `n_clusters` to divide the region may be provided. If not, we choose
as default the maximum number of vehicles we required among each training
instance. This number is estimated as the ratio of total demand and an
individual vehicle's capacity.

References
----------
[1] Bertsimas, Dimitris J., and Garrett Van Ryzin. "Stochastic and dynamic
vehicle routing with general demand and interarrival time distributions."
Advances in Applied Probability (1993): 947-978.

[2] Gillett, Billy E., and Leland R. Miller. "A heuristic algorithm for the
vehicle-dispatch problem." Operations research 22.2 (1974): 340-349. NBR 6023
"""

import logging
import os
from argparse import ArgumentParser
from copy import deepcopy
from dataclasses import dataclass
from multiprocessing import Pool
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
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
class QRPParams:
    num_clusters: Optional[int] = None
    ortools_tsp_params: Optional[ORToolsParams] = None

    @classmethod
    def get_baseline(cls):
        return cls(
            ortools_tsp_params=ORToolsParams(
                max_vehicles=1,
                time_limit_ms=1_000,
            )
        )


@dataclass
class QRPModel:
    params: QRPParams
    cluster_subsolutions: Optional[Dict[int, List[CVRPSolutionVehicle]]] = None
    subinstance: Optional[CVRPInstance] = None
    # Center of all historical packages, used to translate new deliveries and
    # compute their equivalent angles
    center: np.ndarray = np.zeros((0, 2))
    # Angle intervals describing each sub-region. They are described by a
    # `n_cluster` x 2 array with the form
    # [[-pi, angle_1], [angle_1, angle_2], ..., [angle_n, pi]]
    angle_intervals: np.ndarray = np.zeros((0, 2))

    def predict(self, delivery: Delivery) -> int:
        """Predict the best subregion for a given delivery
        Given a set of subregions as angle intervals of the form

            [[-pi, angle_1], [angle_1, angle_2], ..., [angle_n, pi]]

        this method gets the equivalent angle of an incoming delivery and finds
        its appropriate interval.
        """

        point_translated = (
            np.array([delivery.point.lng, delivery.point.lat]) - self.center
        )
        angle = np.arctan2(point_translated[1], point_translated[0])

        # Find the interval where `angle` is greater than the lower limit and
        # smaller than the upper one
        return int(
            np.nonzero(
                (angle >= self.angle_intervals[:, 0])
                & (angle < self.angle_intervals[:, 1])
            )[0]
        )


def pretrain(
    instances: List[CVRPInstance], params: Optional[QRPParams] = None
) -> QRPModel:
    """
    Divide the interval [-pi, +pi] in a number of sub-intervals such that each
    one has the same number of deliveries.

    The number of slices will be defined by default as the maximum number of
    required vehicles among each training instance.

    Notes
    -----
    Given a set of coordinates P:
        1. Compute the center of P;
        2. Translate the coordinates with respect to this center;
        3. Compute the angle in [-pi, +pi] of each translated coordinate with
        respect to a polar system;
        4. Sort the points according to their angle, and divide the final array
        in equal slices. The starting angles in each slice represent the
        subregions.
    """
    params = params or QRPParams()

    points = np.array(
        [
            [d.point.lng, d.point.lat]
            for instance in instances
            for d in instance.deliveries
        ]
    )

    # Compute coordinate angles
    center = points.mean(axis=0)
    points_translated = points - center
    angles = np.arctan2(points_translated[:, 1], points_translated[:, 0])

    # Get number of subregions as the maximum number of vehicles among all
    # training instances if no value is provided
    def _get_number_of_vehicles(instance: CVRPInstance) -> int:
        """Compute required number of vehicles in instance"""
        total_demand = sum(delivery.size for delivery in instance.deliveries)
        return int(np.ceil(total_demand / instance.vehicle_capacity))

    num_clusters = params.num_clusters or min(
        _get_number_of_vehicles(instance) for instance in instances
    )

    # Determine angle intervals in the form
    # [[-pi, angle_1], [angle_1, angle_2], ..., [angle_n, pi]]
    # Notice we need to split into `n + 1` stop-points to get `n` clusters
    split_indices = np.linspace(
        0, angles.size - 1, num_clusters + 1, dtype=int
    )
    sorted_angles = np.sort(angles)
    sorted_angles[0] = -np.pi
    sorted_angles[-1] = np.pi
    angle_intervals = np.vstack(
        (sorted_angles[split_indices[:-1]], sorted_angles[split_indices[1:]])
    ).T

    params.num_clusters = num_clusters
    return QRPModel(
        params=params,
        center=center,
        angle_intervals=angle_intervals,
    )


def finetune(model: QRPModel, instance: CVRPInstance) -> QRPModel:
    """Prepare the model for one particular instance."""

    model_finetuned = deepcopy(model)
    model_finetuned.cluster_subsolutions = {
        i: [] for i in range(model.params.num_clusters)
    }
    model_finetuned.subinstance = instance  # fill a random subinstance

    return model_finetuned


def route(model: QRPModel, delivery: Delivery) -> QRPModel:
    """Route a single delivery using the model instance."""

    cluster = model.predict(delivery)
    subsolution = model.cluster_subsolutions[cluster]

    def is_feasible(route):
        return (
            route.occupation + delivery.size
            < model.subinstance.vehicle_capacity
        )

    # TODO: We could make this method faster by using a route size table, but
    # seems a bit overkill since it's not a bottleneck.
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


def finish(instance: CVRPInstance, model: QRPModel) -> CVRPSolution:

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


def solve_instance(model: QRPModel, instance: CVRPInstance) -> CVRPSolution:
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
