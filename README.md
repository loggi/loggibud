VRPLoggi Benchmark
==================

A dataset and benchmark for last-mile urban logistics.

# Overview

The VRPLoggi benchmark contains a dataset and benchmark scripts for urban logistics problems. The data is from public sources that are highly correlated with actual last-mile deliveries performed by Loggi. Similar to several benchmarks, we also publish a leaderboard of best known solutions.


# Leaderboards

### Capacitated Vehicle Routing Problem

| Submission | Date       | Submitted by             | Solution                            | Distance (km)       |
| ---------- | -----------| ------------------------ | ----------------------------------- | ------------------- |
| ortools1   | 2020/10/31 | Loggi - Network design   | OR-tools VRP \[[code](.)\]          | 10000.000           |
| kmortools1 | 2020/10/31 | Loggi - Network design   | KMeans + OR-tools VRP \[[code](.)\] | 10000.000           |


### Capacitated Vehicle Routing Problem with Stochastic Customers

| Date       | Submitted by             | Solution                     | Test distance (km)       | Train distance (km)       |
| ---------- | ------------------------ | ---------------------------- | ------------------------ | --------------------------|
| 2020/10/31 | Loggi - Network design   | KMeans                       | 10000.000                | 10000.000                 |
| 2020/10/31 | Loggi - Network design   | Sweep                        | 10000.000                | 10000.000                 |


### Routing and Facility location

OR-Tools (p-HUB + VRP)

# Motivation

This benchmark is an effort to make new operations research solutions closer to real-world applications. We believe this work can help both practitioners and academics to reduce the gap between state-of-the-art and practice.

We identify that several interesting solutions in academic literature have evaluation or reproducibility issues. Several papers only include experiments for toy problems that do not resemble real applications. Also, some authors do not publish any code related to the publications, making their work very hard to reproduce.


### Why a new dataset

There are several famous datasets for the Vehicle Routing Problem (VRP). However, there are limitations between these datasets and what can be really applied on real-world last-mile problems.qq

* Small instances
* Ignore streets, use only euclidean distances
* No discussion on aggregation levels


### Why a GitHub benchmark

We want to make publishing results as easy as opening a pull-request. We also want to provide you with code to help you evaluate your solution and make sure it's ready for publication. If you're not familiar with making open-source contributions, don't worry, open an issue and we'll be happy to guide you with your submission.


# How to submit

To include your method to the benchmark leaderboards, you just have to submit the solution data into a pull request. You should provide the data as a JSON file. The schema should match the provided example. We will evaluate your solution with the evaluation script `evaluate.py`. We highly encourage you to run the evaluation script before submission.

While submitting the code is not required, we strongly suggest you to make your research code available to make reproducing the results easier. You can publish the code on your own repository and just include a link on your submission. We also include some baselines on this repository, if you want to include your code as a baseline, we'll be happy to revise it.

Don't forget to acknowledge papers and code you have used on your solution. Use the acknowledgments section for that.

# Instance generation pipeline

If you want more details on how our instances are generated and how they relate to actual deliveries, please check our [generation pipeline documentation](./generation.md). It also includes the steps for reproducing the provided instances.


# Citing this work

If you use this data in academic work, please cite our paper.

```
tex
```

# Disclaimer

This is not an official Loggi product. Use it at your own risk.

# Acknowledgments

[]