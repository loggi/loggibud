import json
from dacite import from_dict
from pathlib import Path

import pandas as pd

from loggibud.v1.baselines.shared import ortools
from loggibud.v1.baselines.task1 import lkh_3
from loggibud.v1.eval.task1 import evaluate_solution
from loggibud.v1.types import CVRPInstance


if __name__ == "__main__":
    file_instances = Path("data/cvrp-instances-1.0/").rglob("*.json")
    solvers = {"ortools": ortools, "lkh-3": lkh_3}
    num_replications = 1

    results_data = []
    for k, file_instance in enumerate(file_instances):
        with open(file_instance, "r") as f:
            data_file = json.load(f)

        instance = from_dict(CVRPInstance, data_file)
        for solver_name, solver in solvers.items():
            for i in range(num_replications):
                print(f"Solver {solver_name} in instance {instance.name}")
                result = solver.solve(instance)
                total_distance = (
                    evaluate_solution(instance, result)
                    if result else -1
                )
                feasible_solution = True if result else False

                results_data.append({
                    "instance_name": instance.name,
                    "instance_size": len(instance.deliveries),
                    "solver": solver_name,
                    "replication": i + 1,
                    "total_distance": total_distance,
                    "feasible_solution": feasible_solution,
                })

        # Stop early here, this must be run in another computer
        # if k >= 30:
            # break

    df_results = pd.DataFrame(results_data)
    df_results.to_csv("task1_results.csv", index=False)
