import json
from argparse import ArgumentParser

from dacite import from_dict

from ..shared.distances import calculate_distance_matrix_m
from .types import CVRPInstance, CVRPSolution, CVRPSolutionVehicle
from .baselines import ortools1


def evaluate_cvrp_solution(instance: CVRPInstance, solution: CVRPSolution):

    # Check if all demands are present.
    solution_demands = set(d for v in solution.vehicles for d in v.deliveries)
    assert solution_demands == set(instance.deliveries)

    # Check if max capacity is respected.
    max_capacity = max(sum(d.size for d in v.deliveries) for v in solution.vehicles)
    assert max_capacity <= instance.vehicle_capacity

    # Compute objective result.
    locations = [instance.origin] + [d.point for d in instance.deliveries]

    # Compute the distance matrix between points.
    distance_matrix = calculate_distance_matrix_m(locations)

    # Build a hash distance map between points.
    distance_map = {
        (s, d): distance_matrix[i, j]
        for i, s in enumerate(locations)
        for j, d in enumerate(locations)
    }

    # Compute the distance for every route circuit.
    route_distances_km = [
        sum(distance_map[s, d] for s, d in zip(v.circuit[:-1], v.circuit[1:])) / 1000.
        for v in solution.vehicles
    ]

    return sum(route_distances_km)


if __name__ == "__main__":
    parser = ArgumentParser()
    
    parser.add_argument('--instance', type=str, required=True)
    parser.add_argument('--solution', type=str, required=True)

    args = parser.parse_args()

    with open(args.instance) as f:
        data = json.load(f)

    instance = from_dict(CVRPInstance, data)

    with open(args.solution) as f:
        data = json.load(f)

    solution = from_dict(CVRPSolution, data)

    print(evaluate_cvrp_solution(instance, solution))