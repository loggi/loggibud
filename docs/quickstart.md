
# Getting started

## Dataset

The full dataset is available to [download here](https://loggibud.s3.amazonaws.com/dataset.zip). Alternativelly, you can generate the instances yourself from public data using the [generation pipeline](./loggibud/v1/instance_generation/README.md).

## OSRM Server

To correctly evaluate distances, you should use OpenStreetMaps distances provided by the OSRM server. Our recommended way of running OSRM is Docker. To run it, please follow these steps.

1. Download and install docker, follow the instructions according to your operational system.
2. Download our [precompiled distance files](https://loggibud.s3.amazonaws.com/osrm/osrm.zip) (5.3Gb compressed, 12.6Gb decompressed).
3. Extract the files into an `osrm` directory.
4. Run an OSRM backend container with the following command:

```
docker run --rm -t -id \
  --name osrm \
  -p 5000:5000 \
  -v "${PWD}/osrm:/data" \
  osrm/osrm-backend osrm-routed --algorithm ch /data/brazil-201110.osrm --max-table-size 10000
```

For more information, check our [OSRM detailed documentation](./docs/osrm.md).

## Python API

We provide an API for loading and running Python solvers.

To implement a new method, we suggest you to implement a Python `solve` function that takes an instance and outputs the solution to a file. 

### Task 1

```python
from loggibud.v1.types import CVRPInstance, CVRPSolution


# Implement your method using a solve function that takes an instance and returns a solution.
def solve(instance: CVRPInstance) -> CVRPSolution:
    return CVRPSolution(...)


# Loading an instance from file.
instance = CVRPInstance.from_file("path/to/instance.json")

# Call your method specific code.
solution = solve(instance)

# Saving your solution to a file.
solution.to_file("path/to/solution.json")
```

To evaluate your solution inside Python, you can do:

```python
from loggibud.v1.eval.task1 import evaluate_solution

distance_km = evaluate_solution(instance, solution)
```

## JSON schemas

If you don't use Python, you should implement your own IO functions. The JSON schemas for reading and writing solutions are described below.

**CVRPInstance**

```javascript
{
  // Name of the specific instance.
  "name": "rj-0-cvrp-0",

  // Hub coordinates, where the vehicles originate.
  "origin": {
    "lng": -42.0,
    "lat": -23.0
  },

  // The capacity (sum of sizes) of every vehicle.
  "vehicle_capacity": 120,

  // The deliveries that should be routed.
  "deliveries": [
    {
      // Unique delivery id.
      "id": "4943245fb66541edaf54f4e3aaed188a",

      // Delivery destination coordinates.
      "point": {
        "lng": -43.12589115884953,
        "lat": -22.89585186478512
      },

      // Size of the delivery.
      "size": 2
    }
    // ...
  ]
}
```

**CVRPSolution**


```javascript
{
  // Name of the specific instance.
  "name": "rj-0-cvrp-0",

  // Hub coordinates, where the vehicles originate.
  "origin": {
    "lng": -42.0,
    "lat": -23.0
  },

  // The capacity (sum of sizes) of every vehicle.
  "vehicle_capacity": 120,

  // The deliveries that should be routed.
  "deliveries": [
    {
      // Unique delivery id.
      "id": "4943245fb66541edaf54f4e3aaed188a",
      
      // Delivery destination coordinates.
      "point": {
        "lng": -43.12589115884953, 
        "lat": -22.89585186478512
      },

      // Size of the delivery.
      "size": 2
    }
    // ...
  ]
}
```

### Evaluation scripts

```bash
python -m loggibud.v1.eval.task1 \
    --instance tests/results/cvrp-instances/train/rj-0-cvrp-0.json \
    --solution results/rj-0-cvrp-0.json
```
# WIP

```
python -m loggibud.v1.baselines.run_task1 \
    --module loggibud.v1.baselines.task1.kmeans_partition_ortools \
    --method solve \
    --instances data/cvrp-instances-1.0/dev/rj-90-cvrp-0.json \
    --output results/

python -m loggibud.v1.eval.task1 \
    --instance tests/results/cvrp-instances/train/rj-0-cvrp-0.json \
    --solution results/rj-0-cvrp-0.json
```
