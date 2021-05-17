from pathlib import Path
from timeit import default_timer

import pandas as pd
from ortools.constraint_solver import routing_enums_pb2

from loggibud.v1.baselines.task2 import kmeans_greedy, qrp_sweep
from loggibud.v1.eval.task1 import evaluate_solution
from loggibud.v1.types import CVRPInstance


if __name__ == "__main__":
    train_paths = Path("data/cvrp-instances-1.0/train/")
    dev_paths = Path("data/cvrp-instances-1.0/dev/")
    solvers = {"kmeans_greedy": kmeans_greedy, "qrp_sweep": qrp_sweep}
    params_dict = {
        "kmeans_greedy": kmeans_greedy.QRPModel(
            ortools_tsp_params=kmeans_greedy.ORToolsParams(
                first_solution_strategy=routing_enums_pb2.
                FirstSolutionStrategy.PATH_CHEAPEST_ARC,
                local_search_metaheuristic=None,
            )
        ),
        "qrp_sweep": qrp_sweep.QRPModel(
            ortools_tsp_params=qrp_sweep.ORToolsParams(
                first_solution_strategy=routing_enums_pb2.
                FirstSolutionStrategy.PATH_CHEAPEST_ARC,
                local_search_metaheuristic=None,
            )
        )
    }

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
            params = params_dict[solver_name]
            model = solver.pretrain(train_instances, params=params)

            # Solve each dev instance with this model
            for dev_instance in dev_instances:
                print(f"Solver {solver_name} in instance {dev_instance.name}")
                try:
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
                        "num_vehicles": len(result.vehicles) if result else -1,
                        "feasible_solution": is_feasible,
                    })
                except TypeError:
                    print(f"Instance {dev_instance.name} has issues so skipped")
                    results_data.append({
                        "instance_name": dev_instance.name,
                        "instance_size": len(dev_instance.deliveries),
                        "solver": solver_name,
                        "total_distance": None,
                        "total_time": None,
                        "num_vehicles": -2,
                        "feasible_solution": -2,
                    })

                # Print results so far
                df_results = pd.DataFrame(results_data)
                df_results.to_csv("task2_results_temp.csv", index=False)

    df_results = pd.DataFrame(results_data)
    df_results.to_csv("task2_results.csv", index=False)
