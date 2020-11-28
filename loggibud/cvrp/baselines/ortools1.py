import logging
import sys
import json
from argparse import ArgumentParser
from datetime import timedelta
from dataclasses import dataclass, asdict
from typing import Optional

import requests
import numpy as np
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from dacite import from_dict

from ...shared.distances import calculate_distance_matrix_m
from ..types import CVRPInstance, CVRPSolution, CVRPSolutionVehicle


logger = logging.getLogger(__name__)


@dataclass
class ORToolsParams:
    first_solution_strategy: int
    local_search_metaheuristic: int
    max_vehicles: Optional[int] = None
    solution_limit: Optional[int] = None
    time_limit_ms: Optional[int] = 300_000

    @classmethod
    def get_base_local_search(cls):
        return cls(
            first_solution_strategy=routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC,
            local_search_metaheuristic=routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH,
        )


def solve_cvrp(
    instance: CVRPInstance,
    params: Optional[ORToolsParams] = None,
    distance_matrix: Optional[np.ndarray] = None,
) -> Optional[CVRPSolution]:
    """Solves a CVRP instance using ORTools"""
    
    # Initialize parameters if not provided.
    params = params or ORToolsParams.get_base_local_search()

    # Number of points is the number of deliveries + the origin.
    num_points = len(instance.deliveries) + 1

    logger.info(f"Solving CVRP instance of size {num_points}.")

    # There's no limit of vehicles, or max(vehicles) = len(deliveries).
    num_vehicles = params.max_vehicles or len(instance.deliveries)

    manager = pywrapcp.RoutingIndexManager(
        num_points,
        num_vehicles,
        0,  # (Number of nodes, Number of vehicles, Origin index).
    )
    model = pywrapcp.RoutingModel(manager)

    # Unwrap the size index for every point.
    sizes = np.array([0] + [d.size for d in instance.deliveries])

    def capacity_callback(src):
        src = manager.IndexToNode(src)
        return int(sizes[src])

    capacity_callback_index = model.RegisterUnaryTransitCallback(capacity_callback)
    model.AddDimension(
        capacity_callback_index, 0, instance.vehicle_capacity, True, "Capacity"
    )

    # Unwrap the location/point for every point.
    locations = [instance.origin] + [d.point for d in instance.deliveries]

    # Compute the distance matrix between points.
    logger.info("Computing distance matrix.")
    distance_matrix = (
        distance_matrix
        if distance_matrix is not None
        else calculate_distance_matrix_m(locations) * 10
    )

    def distance_callback(src, dst):
        x = manager.IndexToNode(src)
        y = manager.IndexToNode(dst)
        return int(distance_matrix[x, y])

    distance_callback_index = model.RegisterTransitCallback(distance_callback)
    model.SetArcCostEvaluatorOfAllVehicles(distance_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = params.first_solution_strategy

    search_parameters.local_search_metaheuristic = params.local_search_metaheuristic

    if params.solution_limit:
        search_parameters.solution_limit = params.solution_limit

    search_parameters.time_limit.FromTimedelta(
        timedelta(microseconds=1e3 * params.time_limit_ms)
    )

    logger.info("Solving CVRP with ORTools.")
    assignment = model.SolveWithParameters(search_parameters)

    # Checking if the feasible solution was found.
    # For more information about the type error:
    # https://developers.google.com/optimization/routing/routing_options
    if not assignment:
            return None

    def extract_solution(vehicle_id):
        # Get the start node for route.
        index = model.Start(vehicle_id)

        # Iterate while we don't reach an end node.
        while not model.IsEnd(assignment.Value(model.NextVar(index))):
            next_index = assignment.Value(model.NextVar(index))
            node = manager.IndexToNode(next_index)

            yield instance.deliveries[node - 1]
            index = next_index

    routes = [
        CVRPSolutionVehicle(
            origin=instance.origin,
            deliveries=list(extract_solution(i)),
        )
        for i in range(num_vehicles)
    ]

    # Return only routes that actually leave the depot.
    return CVRPSolution(
        name=instance.name,
        vehicles=[v for v in routes if len(v.deliveries)],
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = ArgumentParser()
    
    parser.add_argument('--instance', type=str, required=True)
    parser.add_argument('--output', type=str)
    parser.add_argument('--params', type=str)

    args = parser.parse_args()

    with open(args.instance) as f:
        data = json.load(f)

    instance = from_dict(CVRPInstance, data)

    if args.params:
        with open(args.params) as f:
            data = json.load(f)

        params = from_dict(ORToolsParams, data)
    else:
        params = None

    solution = solve_cvrp(instance, params)

    data = asdict(solution)

    with open(args.output or "result.json", "w") as f:
        data = json.dump(data, f)