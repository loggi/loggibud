import json
from dacite import from_dict
from pathlib import Path
from timeit import default_timer

import pandas as pd
from ortools.constraint_solver import routing_enums_pb2

from loggibud.v1.baselines.shared import ortools
from loggibud.v1.eval.task1 import evaluate_solution
from loggibud.v1.types import CVRPInstance


# Number of repetitions for each solver in the same instance
NUM_REPLICATIONS = 1


if __name__ == "__main__":
    file_instances = Path("data/cvrp-instances-1.0/dev/").rglob("*.json")
    solvers = {"ortools": ortools}
    params_dict = {
        "ortools": ortools.ORToolsParams(
            first_solution_strategy=routing_enums_pb2.FirstSolutionStrategy.
            PATH_MOST_CONSTRAINED_ARC,
            local_search_metaheuristic=None,
            time_limit_ms=30 * 60_000,
        ),
    }

    results_data = []
    for k, file_instance in enumerate(file_instances):
        with open(file_instance, "r") as f:
            data_file = json.load(f)

        instance = from_dict(CVRPInstance, data_file)

        for solver_name, solver in solvers.items():
            for i in range(NUM_REPLICATIONS):
                print(f"Solver {solver_name} in instance {instance.name}")
                params = params_dict[solver_name]

                try:
                    tic = default_timer()
                    result = solver.solve(instance)
                    total_time = default_timer() - tic

                    total_distance, is_feasible = (
                        evaluate_solution(instance, result)
                        if result else (-1, False)
                    )

                    if not is_feasible:
                        total_distance = -1

                    results_data.append({
                        "instance_name": instance.name,
                        "instance_size": len(instance.deliveries),
                        "solver": solver_name,
                        "replication": i + 1,
                        "total_distance": total_distance,
                        "total_time": total_time,
                        "num_vehicles": len(result.vehicles) if result else -1,
                        "feasible_solution": is_feasible,
                    })
                except TypeError:
                    print(f"Instance {instance.name} has issues so skipped")
                    results_data.append({
                        "instance_name": instance.name,
                        "instance_size": len(instance.deliveries),
                        "solver": solver_name,
                        "replication": i + 1,
                        "total_distance": None,
                        "total_time": None,
                        "num_vehicles": -2,
                        "feasible_solution": -2,
                    })

        # Print results so far
        df_results = pd.DataFrame(results_data)
        df_results.to_csv("task1_2_results_temp.csv", index=False)

    df_results = pd.DataFrame(results_data)
    df_results.to_csv("task1_2_results.csv", index=False)