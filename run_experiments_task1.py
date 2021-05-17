import json
from dacite import from_dict
from pathlib import Path
from timeit import default_timer

import pandas as pd

from loggibud.v1.baselines.shared import ortools
from loggibud.v1.baselines.task1 import lkh_3
from loggibud.v1.eval.task1 import evaluate_solution
from loggibud.v1.types import CVRPInstance


# Number of repetitions for each solver in the same instance
NUM_REPLICATIONS = 1

# Instances to exclude due to some issue
INSTANCES_TO_EXCLUDE = [
    "cvrp-1-pa-104",  # OSRM matrix returning None when using AWS server
    "cvrp-1-pa-102",  # OSRM matrix returning None when using AWS server
]



if __name__ == "__main__":
    file_instances = Path("data/cvrp-instances-1.0/dev/").rglob("*.json")
    solvers = {"ortools": ortools, "lkh-3": lkh_3}
    params_dict = {
        "ortools": ortools.ORToolsParams(time_limit_ms=20 * 60_000),
        "lkh-3": lkh_3.LKHParams(time_limit_s=20 * 60),
    }

    df_previous = pd.read_csv("task1_results_temp_second_attempt.csv")

    results_data = []
    for k, file_instance in enumerate(file_instances):
        with open(file_instance, "r") as f:
            data_file = json.load(f)

        instance = from_dict(CVRPInstance, data_file)

        if (df_previous["instance_name"] == instance.name).any():
            print(f"Instance {instance.name} already run")
            continue
        
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
        df_results.to_csv("task1_results_temp.csv", index=False)

    df_results = pd.DataFrame(results_data)
    df_results.to_csv("task1_results.csv", index=False)
