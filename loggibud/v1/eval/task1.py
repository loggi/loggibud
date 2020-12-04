import json
from pathlib import Path
from argparse import ArgumentParser
from typing import Union

from ..distances import calculate_distance_matrix_m, calculate_route_distance_m
from ..types import CVRPInstance, CVRPSolution, CVRPSolutionVehicle


def evaluate_cvrp_solution(instance: CVRPInstance, solution: CVRPSolution):

    # Check if all demands are present.
    solution_demands = set(d for v in solution.vehicles for d in v.deliveries)
    assert solution_demands == set(instance.deliveries)

    # Check if max capacity is respected.
    max_capacity = max(sum(d.size for d in v.deliveries) for v in solution.vehicles)
    assert max_capacity <= instance.vehicle_capacity

    route_distances_m = [
        calculate_route_distance_m(v.circuit)
        for v in solution.vehicles
    ]

    # Convert to km.
    return round(sum(route_distances_m) / 1_000, 4)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("--instances", type=str, required=True)
    parser.add_argument("--solutions", type=str, required=True)

    args = parser.parse_args()

    instances_path = Path(args.instances)
    solutions_path = Path(args.solutions)

    if instances_path.is_file() and solutions_path.is_file():
        instances = {"": CVRPInstance.from_file(instances_path)}
        solutions = {"": CVRPSolution.from_file(solutions_path)}

    elif instances_path.is_dir() and solutions_path.is_dir():
        instances = {
            f.stem: CVRPInstance.from_file(f) for f in instances_path.iterdir()
        }
        solutions = {
            f.stem: CVRPSolution.from_file(f) for f in solutions_path.iterdir()
        }

    else:
        raise ValueError("input files do not match, use files or directories.")

    if set(instances) != set(solutions):
        raise ValueError(
            "input files do not match, the solutions and instances should be the same."
        )

    stems = instances.keys()

    results = [
        evaluate_cvrp_solution(instances[stem], solutions[stem]) for stem in stems
    ]

    print(sum(results))
