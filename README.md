Loggi BUD - Benchmark for Urban Deliveries
==================

# Overview

The Loggi Benchmark for Urban Deliveries contains datasets and benchmark scripts for large-scale problems in some of Brazil's largest cities. The data is from public sources that have a high correlation with actual last-mile deliveries performed by Loggi. Similar to several benchmarks, we publish a leaderboard of best-known solutions.

# Dataset

<p float="left">
  <img src="./figures/cvrp_example_1.png" width="100" />
  <img src="./figures/cvrp_example_2.png" width="100" />
  <img src="./figures/cvrp_example_3.png" width="100" />
</p>


# Tasks

### Task 1 - Last-Mile Capacitated Vehicle Routing Problem

This first task is a classic Capacitated Vehicle Routing Problem (CVRP) with minimizing travel distance as objetive. Although solving the CVRP with complete information is often impractical, these solutions are good targets for Task 2.

| Submission | Date       | Submitted by             | Solution                            | Distance (km)       |
| ---------- | -----------| ------------------------ | ----------------------------------- | ------------------- |
| ortools1   | 2020/11/28 | Loggi - Network design   | OR-tools VRP \[[code](.)\]          | 10000.000           |
| kmortools1 | 2020/11/28 | Loggi - Network design   | KMeans + OR-tools VRP \[[code](.)\] | 10000.000           |


### Task 2 - Last-Mile Incremental Capacitated Vehicle Routing Problem

**WIP - COMING SOON**

This is considered a particular case of Stochastic and Dynamic Capacitated Vehicle Routing Problems (SD-CVRP). The objetive is to sort deliveries into routes one by one as they arrive. You may use only historical information and the previously routed deliveries from the same instance. No recombination is allowed after assignment.

From an operations point of view, this solution class is a lot more powerful as it doesn't require full information before start routing. Instead, hub operators can route deliveries as they arrive.


### Task 3 - End-to-end last-mile problem

**WIP - COMING SOON**

This is an extension of the task 1.2, but without fixed dispatch locations. Therefore, locations and allocation of requests to dispatch locations is considered part of the solution, but should be the same accross multiple instances. This can be considered an end-to-end optimization of last-mile delivery operations. In previous tasks, the assignment of demands to hubs is done using an exact solution of a p-hub problem.


# Motivation

This benchmark is an effort to make new operations research solutions closer to real-world applications faced by delivery companies. We believe this work can help both practitioners and academics to reduce the gap between state-of-the-art and practice.

We identify that several promising solutions in academic literature have evaluation or reproducibility issues. Several papers only include experiments for toy problems that do not resemble real applications. Another issue is very few authors in this field publish code related to the publications, which makes their work hard to reproduce.


### Why a new dataset

There are several famous datasets for the Vehicle Routing Problem (VRP). However, there are limitations to these instances that make them hard to apply to real-world last-mile problems. Some of them include:

* Small instances
* Ignore streets, use only euclidean distances
* No discussion on aggregation levels

Most instances also fail to model real challanges of dynamic and stochastic instances, where the stochastic information is usually presented as probabilities on deterministic points. We instead present stochastic information as historical deliveries performed under the same distribution.

### Why a GitHub benchmark

We want to make publishing results as easy as opening a pull-request. We also want to provide you with code to evaluate your solution and make sure it's ready for publication. If you're not familiar with making open-source contributions, don't worry. Open an issue, and we'll be happy to guide you with your submission.


# How to submit

To include your method to the benchmark leaderboards, you must submit the solution data into a pull request. Please check our submission guidelines for more information.

While submitting the code is not required, we strongly suggest making your research code available to make reproducing the results more accessible. You can publish the code on your repository and include a link on your submission. We also have some baselines on this repository. If you want to include your code as a baseline, we'll be happy to revise it.

Don't forget to acknowledge the literature and code you have used on your solution. Use the acknowledgments section for that.

# Instance generation pipeline

If you want more details on how we generate our instances and how they relate to actual deliveries, please check our [generation pipeline documentation](./generation.md). It also includes the steps for reproducing the provided instances.


# Citing this work

If you use this data in academic work, please cite our paper.

```
Coming soon.
```

# Acknowledgments

[]

# Disclaimer

This repository is not an official Loggi product. Use it at your own risk under the terms of the MIT license.

# WIP

```
python -m loggibud.cvrp.baselines.ortools1 \
	--instance tests/results/cvrp-instances/train/rj-0-cvrp-0.json

python -m loggibud.cvrp.eval \
	--instance tests/results/cvrp-instances/train/rj-0-cvrp-0.json \
	--solution result.json
```