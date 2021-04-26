# Run Tasks 1

As an example to execute the LKH method it is necessary to have the input file, and the module that is the strategy to be used, each strategy has a solver and as the standard method will be the "solver" it is possible to create a specific path for the executed output , in addition to being able to add parameters of the class and others.


## LKH

As a test, after having the OSRM server connected to your computer, run:
```
python -m loggibud.v1.baselines.run_task1 --instances data/cvrp-instances-1.0/train/rj-0/cvrp-0-rj-0.json --module loggibud.v1.baselines.task1.lkh_3 --output output/lkh_3/
```

With the output obtained in the `output/lkh_3/` path it is possible to perform the [benchmark](../../../../docs/quickstart.md)

## KMEANS AGGREGATION ORTOOLS

```
python -m loggibud.v1.baselines.run_task1 --instances data/cvrp-instances-1.0/train/rj-0/cvrp-0-rj-0.json --module loggibud.v1.baselines.task1.kmeans_aggregation_ortools --output output/kmeans_aggregation_ortools/
```

With the output obtained in the `output/kmeans_aggregation_ortools/` path it is possible to perform the [benchmark](../../../../docs/quickstart.md)

## KMEANS PARTITION ORTOOLS

As an example to execute the LKH method it is necessary to have the input file, and the module that is the strategy to be used, each strategy has a solver and as the standard method will be the "solver" it is possible to create a specific path for the executed output , in addition to being able to add parameters of the class and others.

As a test, after having the OSRM server connected to your computer, run:
```
python -m loggibud.v1.baselines.run_task1 --instances data/cvrp-instances-1.0/train/rj-0/cvrp-0-rj-0.json --module loggibud.v1.baselines.task1.kmeans_partition_ortools --output output/kmeans_partition_ortools/
```

With the output obtained in the `output/kmeans_partition_ortools/` path it is possible to perform the [benchmark](../../../../docs/quickstart.md)