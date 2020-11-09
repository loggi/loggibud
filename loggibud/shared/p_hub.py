from dataclasses import dataclass

import numpy as np
from ortools.linear_solver import pywraplp as linear_solver


@dataclass
class PHubProblem:
    p: int
    """Number of hubs in the solution."""

    demands: np.ndarray  # shape (n,)
    """Demand units for every demand region."""

    transport_costs: np.ndarray  # shape (n, n)
    """Transportation costs from node i to node j."""


def solve_p_hub(problem: PHubProblem) -> (np.array, np.array):
    """
    Solves a p-hub location problems.
    """

    n_demands = problem.demands.shape[0]
    n_candidates = problem.transport_costs.shape[1]

    solver = linear_solver.Solver(
        "p_hub",
        linear_solver.Solver.CBC_MIXED_INTEGER_PROGRAMMING,
    )

    # Facility decision variable.
    x = {i: solver.BoolVar(f"x{i}") for i in range(n_candidates)}

    # Allocation decision variable.
    y = {
        (i, j): solver.NumVar(0, 1, f"j{i},{j}")
        for i in range(n_candidates)
        for j in range(n_demands)
    }

    # Number of active hubs must be smaller than p.
    solver.Add(sum([x[i] for i in range(n_candidates)]) <= problem.p)

    # All demands must be satisfied.
    for j in range(n_demands):
        solver.Add(sum(y[i, j] for i in range(n_candidates)) == 1)

    # Only active hubs can be selected.
    for i in range(n_candidates):
        for j in range(n_demands):
            solver.Add(y[i, j] <= x[i])

    objective = solver.Objective()

    # Objective is to minimize the cost per unit.
    for i in range(n_candidates):
        for j in range(n_demands):
            objective.SetCoefficient(
                y[i, j], problem.transport_costs[i, j] * problem.demands[j]
            )

    solver.set_time_limit(120_000)
    status = solver.Solve()

    assert status == linear_solver.Solver.OPTIMAL

    # Retrieve the solution decision vars.
    x_sol = np.array(
        [x[i].solution_value() for i in range(n_candidates)], dtype=np.bool
    )

    y_sol = np.array(
        [
            [y[i, j].solution_value() for j in range(n_demands)]
            for i in range(n_candidates)
        ],
        dtype=np.bool,
    )

    return x_sol, y_sol
