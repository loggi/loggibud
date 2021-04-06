from pathlib import Path
from timeit import default_timer

import pandas as pd

from loggibud.v1.baselines.task2 import kmeans_greedy, qrp_sweep
from loggibud.v1.eval.task1 import evaluate_solution
from loggibud.v1.types import CVRPInstance


if __name__ == "__main__":
    train_paths = Path("data/cvrp-instances-1.0/train/")
    dev_paths = Path("data/cvrp-instances-1.0/dev/")
    solvers = {"kmeans_greedy": kmeans_greedy, "qrp_sweep": qrp_sweep}

    results_data = []
    # Iterate at the same time paths "train/df-0" and "dev/df-0", for example
    for train_path, dev_path in zip(
        sorted(train_paths.iterdir()), sorted(dev_paths.iterdir())
    ):
        print(
            f"Now at sets: training {train_path.name} and dev {dev_path.name}"
        )
        train_instances = [
            CVRPInstance.from_file(f) for f in train_path.iterdir()
        ]
        dev_instances = [
            CVRPInstance.from_file(f) for f in dev_path.iterdir()
        ]
        for solver_name, solver in solvers.items():
            # Trains a solver with all test instances in the `train_path`
            model = solver.pretrain(train_instances)

            # Solve each dev instance with this model
            for dev_instance in dev_instances:
                print(f"Solver {solver_name} in instance {dev_instance.name}")
                tic = default_timer()
                result = solver.solve_instance(model, dev_instance)
                total_time = default_timer() - tic

                total_distance, is_feasible = (
                    evaluate_solution(dev_instance, result)
                    if result else (-1, False)
                )

                if not is_feasible:
                    total_distance = -1

                results_data.append({
                    "instance_name": dev_instance.name,
                    "instance_size": len(dev_instance.deliveries),
                    "solver": solver_name,
                    "total_distance": total_distance,
                    "total_time": total_time,
                    "feasible_solution": is_feasible,
                })

                # Print results so far
                df_results = pd.DataFrame(results_data)
                df_results.to_csv("task2_results_temp.csv", index=False)

    df_results = pd.DataFrame(results_data)
    df_results.to_csv("task2_results.csv", index=False)
