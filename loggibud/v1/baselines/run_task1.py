import logging
import os
import importlib
from argparse import ArgumentParser
from pathlib import Path
from multiprocessing import Pool

from tqdm import tqdm

from loggibud.v1.types import CVRPInstance


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    parser = ArgumentParser()

    parser.add_argument("--instances", type=str, required=True)
    parser.add_argument("--module", type=str, required=True)
    parser.add_argument("--method", type=str, default="solve")
    parser.add_argument("--output", type=str)
    parser.add_argument("--params", type=str)
    parser.add_argument("--params_class", type=str)

    args = parser.parse_args()

    # Load method from path.
    module = importlib.import_module(args.module)
    method = getattr(module, args.method)
    params_class = (
        getattr(module, args.params_class) if args.params_class else None
    )

    # Load instance and heuristic params.
    path = Path(args.instances)
    path_dir = path if path.is_dir() else path.parent
    files = [path] if path.is_file() else list(path.iterdir())

    if args.params and not args.params_class:
        raise ValueError(
            "To use custom settings, you must provide both params and params_class."
        )

    params = params_class.from_file(args.params) if args.params else None

    params = None

    output_dir = Path(args.output or ".")
    output_dir.mkdir(parents=True, exist_ok=True)

    def solve(file):
        instance = CVRPInstance.from_file(file)
        solution = method(instance, params)
        solution.to_file(output_dir / f"{instance.name}.json")

    # Run solver on multiprocessing pool.
    with Pool(os.cpu_count()) as pool:
        list(tqdm(pool.imap(solve, files), total=len(files)))
